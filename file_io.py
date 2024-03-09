from datetime import datetime

def save_markdown(task_output):
    today_date = datetime.now().strftime('%Y-%m-%d')

    filename = f"{today_date}.md"

    print("***************************************Description***************************************")
    print(task_output.description)
    print("***************************************RAW OUTPUT***************************************")
    print(task_output.raw_output)
    with open(filename, 'w') as file:
        # file.write(task_output.description)
        file.write(task_output.raw_output)
    print(f"Script saved as {filename}")