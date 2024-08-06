# ESGeePeeTee
ESGeePeeTee is an ESG analysis tool that incorporates almost-real-time news data from GDELT with AutoGluon, an Automated Multi-Layered Stack-Ensembling ML library, to provide powerful, unbiased and accurate ESG score prediction capabilities.

For local deployment:<br />
1. Download the codebase and create a .env file in both the frontend and backend folders with these lines of code:<br />
FRONTEND:<br />
  `VITE_BACKEND_ENDPOINT = <'YOUR BACKEND ENDPOINT HERE'>`<br />
  `VITE_MONGODB_ENDPOINT = <'YOUR MONGODB ENDPOINT HERE'>`<br />
  `VITE_MONGODB_API_KEY = <'YOUR MONGODB API KEY HERE'>`<br />
BACKEND:<br />
  `MONGODB_ENDPOINT = <'YOUR MONGODB ENDPOINT HERE'>`<br />
  `MONGODB_API_KEY = <'YOUR MONGODB API KEY HERE'>`<br />
2. For folders E, S and G (hereby noted as 'dimension') in 'GeePeeTee/backend/model/dimension/AutogluonModels/ag-<somerandomnumber>/metadata.json', adjust these lines of code to your personal OS and Python version details:<br />
`{`<br />
`   "system": <"YOUR OS NAME HERE">,`<br />
`  "version": "1.1.1",`<br />
`  "lite": false,`<br />
`  "py_version": <"YOUR PYTHON VERSION HERE (e.g. 3.11)">,`<br />
`  "py_version_micro": <"YOUR PYTHON MICROVERSION HERE (e.g. 3.11.5)">,`<br />
`  ...`<br />
`}`<br />
P.S.: Autogluon is currently available up to Python 3.11 only<br />

3. Run these commands in frontend/backend folder to start frontend/backend server locally:<br />
FRONTEND:<br />
`  npm run dev`<br />
BACKEND:<br />
`  python server.py`*<br />
<br />P.S.: You may need to download the necessary modules with `pip install` wherever prompted<br />
