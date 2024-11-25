import typing


def question_answer_list_to_dict(qa_list: typing.List[str]):
    if len(qa_list) % 2 == 0:
        raise ValueError("The question/answer list must have odd length.")
    if len(qa_list) == 1:
        return {"str": qa_list[0]}
    return {
        "str": qa_list[0],
        "pass": qa_list[1],
        "rest": question_answer_list_to_dict(qa_list[2:]),
    }
