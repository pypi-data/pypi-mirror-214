def is_valid_body(body):
    if isinstance(body, dict):
        if ("batch" in body or "content" in body) and "metadata" in body:
            return True
    return False


def is_batch_processing(body):
    return "batch" in body
