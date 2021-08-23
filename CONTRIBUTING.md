# Contributing to SkunkBooth
We see that you have decieded to contribute to SkunkBooth and we are excited to have you here ! Take a moment to read our guidelines for :
- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Translating to a new language
- Proposing new features

## We Develop with Github
We use github to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase (we use [Github Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. Run `pre-commit install` to install the pre commit checks
3. If you've added code that should be tested, add tests.
4. If you've added some new documentation.
5. Ensure the test suite passes.
6. Make sure your code lints.
7. Issue that pull request!

## Proposing new features
We always want our app to improve and any help is always appreciated. Open an issue and detail out the new features you are proposing and let us get back to you!
For new filters, you can use one from skunkbooth/filters as a template.

## Discussing the current state of the code
You can use [Discussions](https://github.com/Davidy22/SkunkBooth/discussions) if you want to discuss our code.

## Translating to a new language
In the locales directory, run:
```
mkdir -p {two letter language code}/LC_MESSAGES
cp base.pot {two letter language code}/LC_MESSAGES/base.po
```
And start adding translations to your new base.po file. Once you're done, run locales.sh in the top level of the repository to bake the translation file, and add your language to the drop-down menu in the settings menu in frames.py.

## Any contributions you make will be under the Software License
In short, when you submit code changes, your submissions are understood to be under the same license that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/briandk/transcriptase-atom/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](); it's that easy!

## Write bug reports with detail, background, and sample code
We love simple work, so make sure to keep it simple. Ideally, ensure you:
- Highlight the issue and how to reproduce it.
- Any fixes or workarounds you have tried already.
- A screenshot/video would be really good.

## Use a Consistent Coding Style
Make sure to follow PEP8 standards, also make sure to lint using `black`.

## License
By contributing, you agree that your contributions will be licensed under its License.
