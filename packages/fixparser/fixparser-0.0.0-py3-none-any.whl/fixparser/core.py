import csv


class FIXParser:
    def __init__(self, input_file, output_file, csv_output):
        """
        Initialize the FIXParser with file paths.

        :param input_file: Path to the input file containing FIX messages.
        :param output_file: Path to the human-readable output text file.
        :param csv_output: Path to the output CSV file.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.csv_output = csv_output

    def parse_and_export(self):
        """
        Parse FIX messages from the input file and export to text and CSV formats.
        """
        with open(self.input_file, "r") as infile, \
             open(self.output_file, "w") as outfile, \
             open(self.csv_output, "w", newline="") as csvfile:

            csv_writer = csv.writer(csvfile)

            # Define CSV headers
            headers = [
                "8 (Protocol)", "9 (Body Length)", "35 (Message Type)", "49 (SenderCompID)",
                "56 (TargetCompID)", "34 (MsgSeqNum)", "52 (Sending Time)", "11 (ClOrdID)",
                "38 (OrderQty)", "40 (OrdType)", "54 (Side)", "55 (Symbol)", "44 (Price)",
                "10 (Checksum)"
            ]
            csv_writer.writerow(headers)

            for line in infile:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # Skip empty lines and comments

                # Parse the key-value pairs from the FIX message (comma-separated)
                fields = {}
                for pair in line.split(","):
                    if "=" in pair:
                        key, value = pair.split("=")
                        fields[key] = value

                # Write human-readable output
                output_line = ", ".join([f"{key}: {fields.get(key, 'N/A')}" for key in headers])
                outfile.write(output_line + "\n")

                # Write to CSV
                csv_writer.writerow([fields.get(key.split(" ")[0], "N/A") for key in headers])