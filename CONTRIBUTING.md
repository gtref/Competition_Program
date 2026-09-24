# Contributing

All contributions to this project must be submitted **as email patches**.  
GitHub pull requests are **disabled**.

Follow the steps below.

---

## 1. Fork and Clone

```sh
git clone https://github.com/YOURNAME/Competition_Program.git
cd Competition_Program
```

---

## 2. Create a Branch

```sh
git checkout -b feature/<short-description>
```

---

## 3. Make Your Changes  
Edit code, documentation, or configuration files as needed.

---

## 4. Commit Your Work

```sh
git add .
git commit -s -m "Describe your change here"
```

The `-s` flag adds the **Signed-off-by** line.

---

## 5. Generate a Patch

```sh
git format-patch origin/main
```

This creates one or more `.patch` files.

---

# 6. Run `mailing.py` to See Who to Email

This project includes a helper script:

```
mailing.py
```

It **does not send email**.  
It **does not require any Python dependencies**.  
It simply analyzes your patch and prints:

- The maintainer email  
- Any CC addresses  
- The correct mailing list (if applicable)

Run it like this:

```sh
python mailing.py yourpatch.patch
```

Example:

```sh
python mailing.py 0001-fix-pid.patch
```

It will output something like:

```
Send this patch to: <email>
CC: <other maintainers if detected>
```

---

# 7. Send Your Patch Using `git send-email`

After running `mailing.py` and seeing who to send to, use:

```sh
git send-email yourpatch.patch --to <email-from-mailing.py>
```

If multiple patches:

```sh
git send-email *.patch --to <email-from-mailing.py>
```

---

## 8. Responding to Review

If changes are requested:

1. Fix the code  
2. Commit again with `-s`  
3. Regenerate patches  
4. Run `mailing.py` again  
5. Send the updated patch using `git send-email --in-reply-to=<message-id>`

---

## 9. Coding Style

- Match existing formatting  
- Keep functions small  
- Avoid unnecessary complexity  
- Document anything non-obvious  

---

## 10. Testing

Before sending patches:

- Build the project  
- Ensure no warnings  
- Test robot behavior on hardware if applicable  
