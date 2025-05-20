import os
import win32com.client

# Define the folder to save attachments
SAVE_FOLDER = "C:/Users/vidis/Documents/bizdoc/po_from_mail"  # Replace with your desired folder path
os.makedirs(SAVE_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 refers to the Inbox folder
messages = inbox.Items

print("messages", messages)
# Loop through unread emails and download attachments
for message in messages:
    if message.Class == 43 and message.Subject:  # Ensure it's a mail item with a subject
        print(f"Processing email: {message.Subject}")
        if message.Unread and message.Focused:  # Check if the email is unread and focused
            for attachment in message.Attachments:
                # Save the attachment to the specified folder
                attachment.SaveAsFile(os.path.join(SAVE_FOLDER, attachment.FileName))
                print(f"Saved attachment: {attachment.FileName}")
            message.Unread = False  # Mark the email as read