# Run once by a SharePoint administrator ONLY if BankReport.aspx shows a blank or
# "blocked" page after upload. Requires the SharePoint Online Management Shell:
#   Install-Module -Name Microsoft.Online.SharePoint.PowerShell
#
# Replace <tenant> and <site> with your values, e.g.
#   https://afniah-admin.sharepoint.com  and  https://afniah.sharepoint.com/sites/BankLetters

$AdminUrl = "https://<tenant>-admin.sharepoint.com"
$SiteUrl  = "https://<tenant>.sharepoint.com/sites/<site>"

Connect-SPOService -Url $AdminUrl
Set-SPOSite -Identity $SiteUrl -DenyAddAndCustomizePages $false

# Verify (should print: DenyAddAndCustomizePages : Disabled)
Get-SPOSite -Identity $SiteUrl | Select-Object Url, DenyAddAndCustomizePages
