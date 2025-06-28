# Task: Integrate Transcription Functionality into MediaSlayer

## Objective
Add the ability to download and save video transcripts as clean text files (without timestamps) in the MediaSlayer application.

## Steps

1. **Update Dependencies**
   - Add necessary transcription libraries to `requirements.txt`.

2. **Create Transcription Service**
   - Develop a new service in `mediaslayer/services/transcriber.py`.
   - Extract and adapt logic from existing transcription code.

3. **Update UI Components**
   - Add a "Download Transcript" checkbox and language selection dropdown.
   - Ensure UI updates reflect transcript download status.

4. **Integrate Download Coordination**
   - Modify or create orchestration logic to handle both video and transcript downloads.

5. **Update Main Application Logic**
   - Ensure the main app can handle transcript options and clean text output.

6. **Error Handling & User Experience**
   - Implement clear feedback and error handling for transcript availability.

7. **File Organization**
   - Save transcripts in the same location as videos with a clear naming convention.

## Expected Outcome
- Users can download video transcripts as clean text files alongside video downloads.
- The application remains responsive and user-friendly during the process. 