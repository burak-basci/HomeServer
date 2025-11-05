# Authentication State Persistence Guide

This guide explains how to use Playwright's authentication state persistence feature to avoid logging in every time you run the Adobe Stock upload automation.

## What is Authentication State?

Authentication state includes:
- **Cookies**: Session cookies that keep you logged in
- **localStorage**: Browser storage data
- **sessionStorage**: Session-specific storage
- **Service worker state**: Background sync state

Playwright can save all of this to a single JSON file and reload it in future sessions, making you appear logged in without having to enter credentials again.

## Benefits

✅ **No repeated logins**: Log in once, use forever (until session expires)
✅ **Works with SSO**: Perfect for Google/Facebook/SAML logins
✅ **Works with 2FA**: Authenticate once including 2FA
✅ **Faster execution**: Skip login flow entirely
✅ **More secure**: No need to store passwords in environment variables

## Quick Start

### Step 1: Save Your Authentication State (One Time)

Run the auth saver script with a visible browser:

```bash
python save_adobe_auth.py --no-headless
```

This will:
1. Open a browser window
2. Navigate to Adobe Stock contributor portal
3. Wait for you to log in manually
4. Save your authentication state to `adobe_auth_state.json`

### Step 2: Use Saved Auth in Automated Uploads

Now you can run uploads without logging in:

```bash
python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv
```

The script automatically detects and uses `adobe_auth_state.json` if it exists.

## Advanced Usage

### Custom Auth State File Location

Save to a custom location:

```bash
python save_adobe_auth.py --auth-state /path/to/my_auth.json
```

Use custom auth state in uploads:

```bash
python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv --auth-state /path/to/my_auth.json
```

### Save Auth During Upload

If you prefer to log in during the first upload:

```bash
export ADOBE_USERNAME="your@email.com"
export ADOBE_PASSWORD="yourpassword"
python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv --save-auth
```

This will save the auth state after successful login.

### Multiple Accounts

You can save auth states for multiple Adobe accounts:

```bash
# Account 1
python save_adobe_auth.py --auth-state account1_auth.json

# Account 2
python save_adobe_auth.py --auth-state account2_auth.json

# Use specific account
python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv --auth-state account1_auth.json
```

## How It Works

### Save Flow

```python
# 1. Browser launches
client = AdobeStockPlaywrightAPI()

# 2. You log in manually (or programmatically)
client.login(username, password)

# 3. Save all browser state to JSON
client.save_auth_state("adobe_auth_state.json")
```

The saved JSON file contains:
```json
{
  "cookies": [
    {"name": "session_token", "value": "...", "domain": ".adobe.com", ...},
    ...
  ],
  "origins": [
    {
      "origin": "https://contributor.stock.adobe.com",
      "localStorage": [...],
      ...
    }
  ]
}
```

### Load Flow

```python
# Browser launches with saved state
client = AdobeStockPlaywrightAPI(auth_state_file="adobe_auth_state.json")

# You're already logged in!
client.open_contributor_portal()  # Already authenticated
```

## Troubleshooting

### Auth State Expired

Adobe sessions typically last 30-90 days. If your session expires:

```bash
# Simply re-run the auth saver
python save_adobe_auth.py --no-headless
```

### Auth State Not Working

Check that:
1. The auth state file exists and is valid JSON
2. You logged in successfully before saving
3. You're accessing the same domain (contributor.stock.adobe.com)

Delete the file and re-save if needed:

```bash
rm adobe_auth_state.json
python save_adobe_auth.py --no-headless
```

### Session Sharing Across Machines

You can copy the `adobe_auth_state.json` file to other machines:

```bash
# On machine 1
python save_adobe_auth.py
scp adobe_auth_state.json user@machine2:/path/to/project/

# On machine 2
python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv
```

**Note**: Sessions are tied to your Adobe account, not the machine, so this works fine.

## Security Considerations

⚠️ **Important**: The auth state file contains your login session. Keep it secure!

- **Don't commit to git**: Add `*_auth_state.json` to `.gitignore`
- **Restrict permissions**: `chmod 600 adobe_auth_state.json`
- **Don't share publicly**: This file gives full access to your account
- **Rotate regularly**: Re-save auth state every few weeks

## Integration with CI/CD

For automated deployments:

1. Save auth state locally once
2. Store as encrypted secret in CI/CD (e.g., GitHub Secrets, GitLab CI Variables)
3. Decrypt and use in automated runs

Example for GitHub Actions:

```yaml
- name: Setup Adobe Auth
  run: |
    echo "${{ secrets.ADOBE_AUTH_STATE }}" > adobe_auth_state.json

- name: Upload to Adobe Stock
  run: |
    python upload_adobe_stock_playwright.py ./images ./metadata.csv --headless
```

## Comparison with Other Auth Methods

| Method | Pros | Cons |
|--------|------|------|
| **Auth State File** | ✅ Works with SSO<br>✅ Works with 2FA<br>✅ Fast<br>✅ Secure | ❌ Requires manual setup<br>❌ Session expires |
| **Environment Variables** | ✅ Fully automated<br>✅ Easy setup | ❌ Doesn't work with SSO<br>❌ Doesn't work with 2FA<br>❌ Less secure |
| **Profile Directory** | ✅ Persistent<br>✅ Browser-native | ❌ Machine-specific<br>❌ Can't share<br>❌ Larger files |

## Next Steps

- Run `python save_adobe_auth.py --no-headless` to save your auth state
- Test with `python upload_adobe_stock_playwright.py` using sample images
- Automate your workflow with n8n or cron jobs!
