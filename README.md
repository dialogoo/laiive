# Laiive

<img width="90" height="90" alt="laiive1" src="https://github.com/user-attachments/assets/357725b4-4da2-4463-b9a5-896a29fc4b79" />

#### what is 🫦Laiive
Laiive is the best way to know what to do, Laiive connect live music places with people. Laiive is a link between life music and public. Just ask, Laiive will answer.[^*]

![mockup](https://github.com/user-attachments/assets/4f94c5df-6b66-42b8-9925-1314b9987c48)

#### why is 🫦Laiive needed?
laiive links the broken connection between events and public[^*]

![mission](https://github.com/user-attachments/assets/569506fc-6adb-4762-8b60-2f2e0bb69866)

#### why 🫦Laiive makes sense?
1st Assumption: Music or event organizers will upload their events KEYPOINT (value is the event promoters getting used to this) problem: upload without seeing the result.
2nd Assumption: People will check in the chat what to do, and system will answer friendly.
3rd Assumption; with all the events there people will recommend it to friends and make it viral (growth model)

#### why is 🫦Laiive good?

#### why is 🫦Laiive  profitable?

---

## Services
<img width="90" height="90" alt="laiive1" src="https://github.com/user-attachments/assets/f8dc0267-f630-4a87-b3f8-fe0277137ba5"  />

### UI
a ZERO CLIC UI is the public view of laiive
1st phase:  MVP minimal viable product, streamlit easy app or similar (python base)
2nd phase: jump into React frontend

### RAG-chat
With a simple UI this is the backbone of laiive, high accuracy on retrievals from the knwoledge database is a must
1st phase: with llama-index just session id, no user id. just serving info, not extracting info from conversations
2nd phase. + user id

### Event Scraper
First feed to the db, until the pusher will the main data source and the system is ready to switch
The transition will be based on geographic penetration.

### Pusher-Extractor
Easy is the keyword, the most easy way to push and confirm your event data.
Optimized for reliability. A reliable database serves reliable answers.

### Data
laiive deals with ephimeral data, data that still doesn't exist, laiive is a dynamic process, that grows in inertia when users use it and promoters push events.
A Postgres db is the heart of this dynamics and stores all the system knowledge.

---

[^*]: © laiive. All strategic documents, diagrams, mockups, and planning materials contained in this repository are the intellectual property of Laiive and are provided solely for reference purposes. Unauthorized reproduction, distribution, reverse engineering, or commercial use of these materials is strictly prohibited without prior written consent from Laiive. For questions regarding usage rights or licensing, please contact: info@laiive.com.



### instructions

#### Development Setup in devcontainer (recommended)

1. Open the devcontainer: (instructions for VScode)
   ```bash
   # From the root directory
   code .
   # Then click "Reopen in Container" when prompted
   ```
   alternatively Ctrl+shift+P "DevContainer: Rebuild and reopen in Container"

2. Navigate to desired service directory and install dependencies:
   ```bash
   cd services/<service-name>
   uv sync  # Install Python dependencies using uv
   ```
   alternatively use the Makefile command
   ```bash
   make deps
   ```

3. Start the development server:
   ```bash
   make dev  # Run the service in development mode
   ```

4. Open localhost:3001 and localhost:8001 to check or use the services ports
