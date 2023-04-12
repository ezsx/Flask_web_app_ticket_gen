# Balanced Tickets Generator

#### (still in progress)

#### This project is a web application for generating balanced tickets, where each ticket contains two theoretical and one practical questions. The goal is to create tickets with similar difficulty levels.

## Features
 1. Import theoretical and practical questions from Word documents.
 2. Edit the difficulty level and text of each question.
 3. Generate a specified number of balanced tickets with a given target difficulty.
 4. View generated tickets and save them as a Word document.

## Usage
1. Import questions from Word documents by clicking on "Choose File" on the ticket generation page. Theoretical questions should be in one file, and practical questions in another. You can upload multiple files if needed. The format of the Word document should have the question type specified at the beginning of the file, followed by the question text.
2. Edit the difficulty level and text of each question using the provided form.
3. Specify the desired number of tickets and the target difficulty for each ticket. The algorithm will try to generate tickets with the specified difficulty.
4. The generated tickets will be displayed on the "Generated Tickets" section. You can view the result and save it as a Word document.

## Notes
* The generator currently requires each ticket to have two theoretical questions and one practical question.
* To generate more tickets, add more questions with varying difficulties.
* The algorithm will try to generate tickets with a difficulty level as close as possible to the target difficulty. However, it may not always be possible to create a ticket that matches the target difficulty exactly.
