import csv

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

def export_to_csv(networks, filepath):
    if not networks:
        raise ValueError("No network data to export.")
    fieldnames = ["SSID", "BSSID", "Signal", "Channel", "Security"]
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for net in networks:
            writer.writerow({
                "SSID": net.get("ssid", ""),
                "BSSID": net.get("bssid", ""),
                "Signal": net.get("signal", ""),
                "Channel": net.get("channel", ""),
                "Security": net.get("security", "")
            })

def export_to_pdf(networks, filepath):
    if FPDF is None:
        raise ImportError("fpdf library is not installed. Run 'pip install fpdf'.")

    if not networks:
        raise ValueError("No network data to export.")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    col_widths = [40, 40, 20, 20, 40]
    headers = ["SSID", "BSSID", "Signal", "Channel", "Security"]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1)
    pdf.ln()

    for net in networks:
        pdf.cell(col_widths[0], 10, str(net.get("ssid", "")), border=1)
        pdf.cell(col_widths[1], 10, str(net.get("bssid", "")), border=1)
        pdf.cell(col_widths[2], 10, str(net.get("signal", "")), border=1)
        pdf.cell(col_widths[3], 10, str(net.get("channel", "")), border=1)
        pdf.cell(col_widths[4], 10, str(net.get("security", "")), border=1)
        pdf.ln()

    pdf.output(filepath)

def export_networks(networks, filepath, filetype="csv"):
    if filetype.lower() == "csv":
        export_to_csv(networks, filepath)
    elif filetype.lower() == "pdf":
        export_to_pdf(networks, filepath)
    else:
        raise ValueError("Unsupported file type. Use 'csv' or 'pdf'.")
