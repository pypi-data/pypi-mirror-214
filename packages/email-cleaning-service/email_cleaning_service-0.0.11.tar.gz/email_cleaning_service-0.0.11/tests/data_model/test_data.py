import email_cleaning_service.data_model.data as data

def test_EmailMessage():
    lines = [
        "This is a test email. I am testing the email cleaner.",
        "This is another line",
        "Yet another line"
    ]
    sections = [4, 5, 6]
    email_message = data.EmailMessage(lines)
    email_message.set_sections(sections)

    assert email_message.get("body") == "This is a test email. I am testing the email cleaner."
    assert email_message.get("signature") == "This is another line"

def test_EmailThread():
    email = "This is a long email.\nIt has a lot of lines. \nIt is a test email."

    email_thread = data.EmailThread(email)

    email_thread.segment([4, 5, 6], [0, 1, 0])

    assert email_thread.get_label_sequences(seq_len=2) == [[0, 1], [0, 0]]
    assert email_thread.messages[0].get("body") == "This is a long email."
    assert len(email_thread.messages) == 2