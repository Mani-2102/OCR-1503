import { useState } from "react";
import axios from "axios";

function InvoiceUploader() {
    const [invoicePath, setInvoicePath] = useState("");
    const [invoiceData, setInvoiceData] = useState({});

    const handleRunOCR = async () => {
        const response = await axios.post("http://127.0.0.1:8000/process_invoice", { path: invoicePath });
        setInvoiceData(response.data);
    };

    return (
        <div>
            <input
                type="text" 
                placeholder="Enter Invoice Path" 
                value={invoicePath} 
                onChange={(e) => setInvoicePath(e.target.value)} 
            />
            <button onClick={handleRunOCR}>Run</button>

            {invoiceData.invoice_number && (
                <div>
                    <p>Invoice Number: {invoiceData.invoice_number}</p>
                    <p>Invoice Date: {invoiceData.invoice_date}</p>
                    <p>PO Number: {invoiceData.po_number}</p>
                    <p>Total: {invoiceData.total}</p>
                    <p>Vendor Name: {invoiceData.vendor_name}</p>
                </div>
            )}
        </div>
    );
}

export default InvoiceUploader;
