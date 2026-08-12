from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
css = (ROOT / 'styles.css').read_text(encoding='utf-8')
view_text = (ROOT / 'sequence_views.py').read_text(encoding='utf-8')

required_css = [
    'min-height: 92px',
    '.choice-direct:has(input:focus-visible)',
    '.choice:has(input:checked)',
    'touch-action: manipulation',
    '@media (max-width: 540px)',
]
for marker in required_css:
    assert marker in css, marker

for marker in ['role="group"', 'aria-label="Réponses proposées"', 'aria-live="polite"', 'role="alert"']:
    assert marker in view_text, marker

spec = importlib.util.spec_from_file_location('sequence_views', ROOT / 'sequence_views.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
question = {
    'type': 'single_choice',
    'choices': {'A': 'un', 'B': 'deux', 'C': 'trois', 'D': 'quatre'},
}
html = module._choices(question)
assert html.count('choice-direct') == 4
assert html.count('type="radio"') == 4
assert 'onchange=' not in html
assert all(f'choice-letter">{letter}<' in html for letter in 'ABCD')

page = module.question_page(
    lambda _title, body: body,
    {},
    'csrf-token',
    {'id': 1, 'current_index': 0, 'total_questions': 1, 'level': 'A0'},
    {'slug': 'sequence-1', 'title': 'Séquence 1'},
    {
        **question,
        'id': 'S1-A0-001',
        'competency': 'Test',
        'instruction': 'Choisir',
        'support': '',
        'help': 'Aide',
    },
)
assert '<button type="submit">Valider ma réponse</button>' in page
print('INTERFACE_CHECK_OK')
