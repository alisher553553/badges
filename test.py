import csv
import qrcode  # type: ignore
import os

# File paths
file_path = r'C:\Users\alish\OneDrive - Concordia University - Canada\Desktop\courses\fall 2024\Logisticsathack2025\Participant_Sample_Updated.csv'
output_dir = r'C:\Users\alish\OneDrive - Concordia University - Canada\Desktop\courses\fall 2024\Logisticsathack2025\QR_Output'

# Base URL for QR_CODE_VALUE
base_url = "https://athackctf.com/participantInfo/qrcode="

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Open and read the CSV file
with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    print("CSV Headers:", reader.fieldnames)  # Debug headers

    for index, row in enumerate(reader, start=1):
        participant_name = row['Participant Name'].strip()
        qr_code_value = row['QR_CODE_VALUE'].strip()  # Unique ID for the participant
        qr_code_filename = row['QR_CODE_FILENAME'].strip()

        # Validate filename and append .png if missing
        if not qr_code_filename:
            qr_code_filename = f"{participant_name}_QR.png"
        elif not qr_code_filename.endswith('.png'):
            qr_code_filename += '.png'

        qr_code_filename = os.path.join(output_dir, qr_code_filename)
        print(f"Saving QR code image to: {qr_code_filename}")

        # Check if participant_name or QR_CODE_VALUE is empty
        if not participant_name or not qr_code_value:
            print(f"Skipping row {index} due to missing participant name or QR_CODE_VALUE.")
            continue

        # Create the full URL with the QR_CODE_VALUE
        full_url = base_url + qr_code_value

        # Debugging output
        print(f"Adding to QR code: {full_url}")

        # Generate QR code with the full URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(full_url)
        qr.make(fit=True)

        # Save QR code image
        try:
            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((600, 600))  # Optional: test without resizing
            img.save(qr_code_filename)
            print(f"Generated QR code for {participant_name} as {qr_code_filename}")
        except Exception as e:
            print(f"Error saving QR code for {participant_name}: {e}")