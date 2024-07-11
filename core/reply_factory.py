
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    correct_answer = PYTHON_QUESTION_LIST[current_question_id]["correct_answer"]
    if answer.strip().lower() == correct_answer.strip().lower():
        session["score"] = session.get("score", 0) + 1
        return True, "Correct answer!"
    else:
        return True, f"Sorry, the correct answer was {correct_answer}."




def get_next_question(current_question_id):
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id], next_question_id
    else:
        return None, None




def generate_final_response(session):
    score = session.get("score", 0)
    total_questions = len(PYTHON_QUESTION_LIST)
    final_message = f"Your final score is {score} out of {total_questions}."
    return final_message


    
