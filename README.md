# Bank Financing Request Letter – SharePoint page

صفحة ويب ذاتية الاحتواء (ملف واحد) تولّد خطاب **طلب تمويل بنكي** بنفس تخطيط وخط الخطاب النموذجي
(ورق أفنية الرسمي + خط Sakkal Majalla + أرقام Calibri)، مع تفقيط تلقائي للمبلغ وفق معيار
[tafqit.com](https://tafqit.com/) بالصيغة القانونية «فقط … لا غير».

A self-contained, single-file web page that generates the **bank financing request letter**
with the exact layout and fonts of the sample letter (Afniah letterhead, Sakkal Majalla for
Arabic, Calibri for digits). The amount is converted to Arabic words automatically using the
[tafqit.com](https://tafqit.com/) standard in legal form ("فقط … لا غير").

## What the page does

- **Three financing types**: Islamic Financing (تمويل إسلامي – تسهيلات رواتب),
  Invoice Financing (تمويل فواتير), Government Invoice (فاتورة حكومية). Picking a type
  loads that type's default subject, facility name, repayment period and body text.
- **Fixed values** that never change: company (شركة أفنية للاستشارات الهندسية), CR number
  (2051059942) and addressee (بنك الرياض). The bank account is chosen from two fixed
  accounts: 3530002069940 or 3013466169940.
- **Editable numeric values**: amount, repayment period and unit. The government-invoice
  type adds invoice number, entity and invoice date.
- **Automatic Arabic amount in words** (tafqit.com standard, legal form), e.g.
  `785,000` → `فقط سبعمائة وخمسة وثمانون ألف ريال سعودي لا غير`. Halalas are supported.
- **Editable letter details**: date, reference number, subject, facility name, signatory
  title and name, and the full body text template.
- **Live A4 preview** on the letterhead. The letterhead can be left out when printing on
  pre-printed paper.
- **Download as Word (.docx)**. The file is built from the original letterhead template
  (`letter_head.docx`, A4) with Sakkal Majalla for Arabic and Calibri for digits, so it opens
  in Word ready to edit, sign and print. The browser print dialog is also available. Values
  are remembered in the browser (localStorage).

## Files

| Path | Purpose |
| --- | --- |
| `dist/BankReport.aspx` | **Upload this to SharePoint.** Single file, everything inlined. |
| `dist/BankReport.html` | Same page for any other host, or to open locally. |
| `dist/BankReport.artifact.html` | Variant published as a Claude artifact (no document skeleton; the Word file is offered through the viewer's save prompt). |
| `src/index.html` | Page source (HTML, CSS, JS). |
| `src/tafqit.js` | Arabic number-to-words library by Mohsen Alyafei (MIT), the engine behind tafqit.com. |
| `src/jszip.min.js` | JSZip 3.10.1 (MIT), used to assemble the .docx in the browser. |
| `assets/letterhead.jpg` | Letterhead extracted from `letter_head.docx` (preview background). |
| `assets/letter_template.docx` | `letter_head.docx` with the letterhead sized to a full A4 page; the Word export fills its body. |
| `build.py` | Rebuilds `dist/` from `src/` and `assets/` (Python 3, no dependencies). |

## Adding the page to SharePoint

SharePoint Online downloads `.html` files instead of showing them, so the page is also
provided as `BankReport.aspx`, which SharePoint renders in the browser.

### Option A – upload to the site (simplest)

1. In your SharePoint site open **Site contents → Site Assets** (or any document library).
2. Upload `dist/BankReport.aspx`.
3. Open the file. Its URL is the page you share with colleagues, for example
   `https://<tenant>.sharepoint.com/sites/<site>/SiteAssets/BankReport.aspx`.
4. Optional: add that link to the site navigation, or add a **Button** / **Quick links**
   web part on a modern page that points to it.

The page contains JavaScript, so the site must allow **custom script**. If opening the file
shows a blocked or blank page, a SharePoint administrator runs once (SharePoint Online
Management Shell):

```powershell
Connect-SPOService -Url https://<tenant>-admin.sharepoint.com
Set-SPOSite -Identity https://<tenant>.sharepoint.com/sites/<site> -DenyAddAndCustomizePages $false
```

Microsoft may reset this setting on some tenants after 24 hours. If that happens, use
option B.

### Option B – host the file elsewhere and embed it

1. Host `dist/BankReport.html` on any HTTPS site your organisation controls
   (for example an Azure Static Web App, GitHub Pages, or an IIS server).
2. On a modern SharePoint page add the **Embed** web part and paste the page URL.
3. If SharePoint refuses the URL, a site owner adds the domain under
   **Site settings → HTML Field Security**.

### Fonts

The letter uses **Sakkal Majalla** (Arabic) and **Calibri** (digits), both shipped with
Windows and Microsoft 365, so on company PCs the output matches the sample exactly. On
machines without those fonts the page falls back to Noto Naskh Arabic and Carlito, which are
loaded from Google Fonts.

## Output

Click **تنزيل ملف Word** to download the letter as `.docx`. Untick "تضمين الورق الرسمي" to
get a file without the letterhead image, for printing on pre-printed paper. The letter has
no signature image; it is signed by hand or in Word. **طباعة** opens the browser print
dialog (choose A4, margins None).

## Editing the wording

Each financing type has its own body text template in the panel. Placeholders in curly
braces are replaced automatically:

```
{amount} {amountWords} {cr} {bank} {facility} {period} {periodUnit}
{account} {company} {invoiceNo} {entity} {invoiceDate}
```

"استعادة النص الافتراضي" restores the built-in text for that type. To change the built-in
defaults permanently, edit `TYPES`, `STD_TEMPLATE` and `GOV_TEMPLATE` in `src/index.html`
and run `python3 build.py`. The fixed company, CR, bank and account list are `FIXED` and
`ACCOUNTS` in the same file.

## Rebuilding

```bash
python3 build.py   # writes dist/BankReport.html and dist/BankReport.aspx
```
