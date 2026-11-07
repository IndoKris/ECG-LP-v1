# ECG Portal: V1 Prototype PRD

## Goal

Test whether a vision AI model can read ECG images well enough to help teach medical students. Build a small quiz around it and see how students and the AI compare.

## Scope

| In V1 | Not in V1 |
|---|---|
| 48 ECG images from PTB-XL | Student uploads |
| One vision AI model, no training | Model training or fine-tuning |
| One static quiz page, 10 questions | Accounts, database, backend |
| Test with 5 to 10 friends | Public launch |

The correct answer is always the cardiologist label in the dataset. The AI is a second opinion and can be wrong.

## Tools

Python, `wfdb`, `pandas`, `numpy`, `matplotlib`, `scikit-learn`, one vision AI model API, plain HTML and JavaScript.

## Steps

### Step 1: Download PTB-XL and pick 48 records

- Download PTB-XL from PhysioNet. Install: `pip install wfdb pandas numpy matplotlib scikit-learn`.
- Open `ptbxl_database.csv` and `scp_statements.csv` with pandas.
- Keep only records where `validated_by_human` is true, the label likelihood in `scp_codes` is 100, there is a single diagnosis, and each patient appears once.
- Pick 8 records for each of 6 classes (48 total):

| Class | PTB-XL code (verify in `scp_statements.csv`) |
|---|---|
| Normal | NORM |
| Atrial fibrillation | AFIB |
| Left bundle branch block | CLBBB |
| Right bundle branch block | CRBBB |
| Inferior myocardial infarction | IMI |
| First-degree AV block | 1AVB |

- **Output:** `selected.csv` with record ID, file path and true label.
- **Done when:** the file lists 48 records, 8 per class.

### Step 2: Run the script to make 48 ECG images

- Read each record with `wfdb.rdsamp`. Check the file path column names in the CSV.
- Plot 12 leads in a 3 by 4 layout, plus a long lead II strip. Use a grid, 25 mm/s and 10 mm/mV.
- Do not write the diagnosis on the image. Save each image under a random file name.
- Keep the answer key in a separate file, `answer_key.csv`.
- Option: use ECG-Image-Kit instead of writing your own plot.
- **Output:** `images/` with 48 PNG files, and `answer_key.csv`.
- **Done when:** you have opened every image and none look broken or unreadable.

### Step 3: Send each image to a vision AI model and save its answer

- A vision AI model takes an image plus a text question and replies in text. You do not train it.
- Use one fixed prompt. Ask it to reply in JSON with: rhythm, heart rate, the best match from the 6 classes (or "other"), its top 3 guesses with confidence, and a short reason.
- Test with 5 images first to check the output format and cost.
- Loop over all images. Save each answer to `ai_answers.json`. Skip images already done. Add a short pause and retries for rate-limit errors.
- Check the API docs for image size limits and rate limits.
- **Output:** `ai_answers.json`.
- **Done when:** all 48 images have an answer.

### Step 4: Compare its answers with the real labels

- Compute with scikit-learn: overall accuracy, top-3 accuracy, accuracy per class, and a confusion matrix.
- Tune the prompt on 16 images only. Calculate the final score on the other 32.
- Read every wrong answer and note why it failed.
- **Output:** `results.md` with the scores and notes on wrong cases.
- **Done when:** you know how often the AI is right and which classes it misses.

### Step 5: Ask a medical student to check a few images and the AI's answers

- Give them 15 images with the AI's answers.
- Ask three questions per image: Does the image look like a real ECG? Is the label plausible? Is the AI's reason correct?
- **Output:** a short table of their answers.
- **Done when:** you know if the images and the AI's explanations are good enough to show students.

### Step 6: Build the quiz as a single static page

- Files: `index.html`, `images/`, and the quiz data inside the page (or `quiz_data.json`).
- Pick 10 images, mixed across the 6 classes.
- Each question shows one image and 4 options: the correct class plus 3 others.
- After the student answers, show right or wrong from the true label, then the AI's answer and explanation.
- Optional: a text box for the student's reasoning.
- Show a disclaimer: for education only, not for diagnosing patients.
- A static page cannot save results. Ask friends to send a screenshot of their score, or add a Google Form later.
- Host it on GitHub Pages, or send the folder.
- **Output:** a working quiz page.
- **Done when:** you can finish all 10 questions without errors on a phone and a laptop.

### Step 7: Share with friends and see their results

- Share with 5 to 10 friends.
- Collect: score, questions missed, and whether the AI's feedback helped.
- Compare student accuracy with AI accuracy.
- **Output:** a short findings note.

## Decision after Step 7

| Result | Next move |
|---|---|
| AI is right on most images and friends find it useful | Build V2: uploads, more cases |
| AI is right on some classes only | Improve the prompt or try a different model |
| AI is mostly wrong | Keep the quiz with expert explanations, drop AI reading for now |

Suggested bar for "right on most images": 70% or more. Change it after talking to a medical reviewer.

## Notes

- Nothing here has been run or tested. Check tool names, column names and PTB-XL codes before you start.
- Time estimates are not included. Plan for roughly 2 weeks part-time.
- This is an educational prototype. It must not be used to diagnose or treat real patients.
