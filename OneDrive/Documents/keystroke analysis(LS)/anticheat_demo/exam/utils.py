def analyze_keystrokes(keystroke_data, start_time, end_time, answer_text):
    events = keystroke_data.get("events", [])
    backspaces = keystroke_data.get("backspaceCount", 0)
    max_chunk = keystroke_data.get("maxChunk", 0)
    big_chunk_count = keystroke_data.get("bigChunkCount", 0)
    idle_times = keystroke_data.get("idleTimes", [])
    paste_detected = keystroke_data.get("pasteDetected", False)

    try:
        total_time_sec = (int(end_time) - int(start_time)) / 1000
    except:
        total_time_sec = 0

    total_chars = len(answer_text)
    event_count = len(events)

    risk = 0

    # 1) Paste flag
    if paste_detected:
        risk += 50

    # 2) Speed check
    if total_time_sec > 0:
        chars_per_sec = total_chars / total_time_sec
        if chars_per_sec > 8:
            risk += 30

    # 3) Big chunk insert
    if max_chunk > 20:
        risk += 40

    if big_chunk_count > 2:
        risk += 20

    # 4) No edits in long answer
    if total_chars > 200 and backspaces == 0:
        risk += 20

    # 5) Event density (paste = few events, long text)
    if event_count > 0 and total_chars / event_count > 15:
        risk += 20

    # 6) Idle time pattern: very long idle + sudden big text
    if idle_times and max(idle_times) > 5000 and max_chunk > 20:
        risk += 20

    # 7) Minimum time rule (sanity check)
    if total_chars > 300 and total_time_sec < 60:  # 300 chars in < 1 min
        risk += 30

    # Cap at 100
    return min(risk, 100)









# def analyze_keystrokes(keystroke_data, start_time, end_time, answer_text):
#     events = keystroke_data.get("events", [])
#     backspaces = keystroke_data.get("backspaceCount", 0)

#     try:
#         total_time_sec = (int(end_time) - int(start_time)) / 1000
#     except:
#         total_time_sec = 0

#     total_chars = len(answer_text)

#     risk = 0

#     # Speed check
#     if total_time_sec > 0:
#         chars_per_sec = total_chars / total_time_sec
#         if chars_per_sec > 8:
#             risk += 30

#     # Chunk insert check
#     big_chunks = [e for e in events if e.get("deltaLength", 0) > 20]
#     if big_chunks:
#         risk += 40

#     # No edits in long answer
#     if total_chars > 200 and backspaces == 0:
#         risk += 20

#     # Few events but long text
#     if len(events) < max(1, total_chars // 10):
#         risk += 20

#     return min(risk, 100)