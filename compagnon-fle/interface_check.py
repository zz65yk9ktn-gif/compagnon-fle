from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
css = (ROOT / 'styles.css').read_text(encoding='utf-8')
view_text = (ROOT / 'sequence_views.py').read_text(encoding='utf-8')
server_text = (ROOT / 'server.py').read_text(encoding='utf-8')

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

for marker in ['notice-error" role="alert"', 'aria-describedby="password-rules"', 'id="password-rules"']:
    assert marker in server_text, marker

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
assert '<button type="submit">Valider</button>' in page
assert '<summary>Aide</summary>' in page

feedback = module.feedback_page(
    lambda _title, body: body,
    {},
    {'current_index': 1, 'total_questions': 5, 'status': 'in_progress'},
    {'slug': 'sequence-6', 'title': 'Séquence 6'},
    {'feedback_success': 'Bravo', 'feedback_error': 'Erreur', 'correct_answer': 'A', 'choices': {'A': 'Oui'}},
    {'requires_manual_review': False, 'is_correct': True},
)
assert 'href="/espace-apprenant/sequence-6/demarrer">Suivant</a>' in feedback

result = module.result_page(
    lambda _title, body: body,
    {},
    {'level': 'A0', 'evaluated_count': 5, 'success_count': 5, 'score_percentage': 100, 'manual_review_count': 0},
    {'slug': 'sequence-6', 'title': 'Séquence 6'},
)
assert 'href="/espace-apprenant/sequence-6/demarrer?nouvelle=1">Commencer une nouvelle série</a>' in result
print('INTERFACE_CHECK_OK')
