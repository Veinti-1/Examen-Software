const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();

app.use(express.json());

const port = 8080;
const daprPort = process.env.DAPR_HTTP_PORT ?? 3500;

const daprUrl = `http://localhost:${daprPort}/v1.0/invoke`;

// The name of the state store is specified in the components yaml file. 
// For this sample, state store name is specified in the file at: https://github.com/dapr/quickstarts/blob/master/hello-kubernetes/deploy/redis.yaml#L4
const stateStoreName = `statestore`;
const stateUrl = `http://localhost:${daprPort}/v1.0/state/${stateStoreName}`;

/**
The following routes forward requests (using pipe) from our React client to our dapr-enabled services. Our Dapr sidecar lives on localhost:<daprPort>. We invoke other Dapr enabled services by calling /v1.0/invoke/<DAPR_ID>/method/<SERVICE'S_ROUTE>.
*/

app.post('/votaciones/candidates', async (req, res) => {
  try {

      const appResponse = await axios.post(`${daprUrl}/votacionesapp/method/candidates`, req.body);

      // Return expected string result to client
      return res.send(`${appResponse.data}`); 
  } catch (err) {
      console.log(err);
  }
});

app.post('/votaciones/close-creation-phase', async (req, res) => {
  try {

      const appResponse = await axios.post(`${daprUrl}/votacionesapp/method/close-creation-phase`, req.body);
      
      // Return expected string result to client
      return res.send(`${appResponse.data}`); 
  } catch (err) {
      console.log(err);
  }
});

app.post('/votaciones/vote', async (req, res) => {
  try {

      const appResponse = await axios.post(`${daprUrl}/votacionesapp/method/vote`, req.body);

      // Return expected string result to client
      return res.send(`${appResponse.data}`); 
  } catch (err) {
      console.log(err);
  }
});

app.post('/votaciones/close-voting-phase', async (req, res) => {
  try {

      const appResponse = await axios.post(`${daprUrl}/votacionesapp/method/close-voting-phase`, req.body);

      // Return expected string result to client
      return res.send(`${appResponse.data}`); 
  } catch (err) {
      console.log(err);
  }
});

app.post('/votaciones/stats', async (req, res) => {
    try {

        const appResponse = await axios.post(`${daprUrl}/votacionesapp/method/stats`, req.body);
  
        // Return expected string result to client
        return res.send(`${appResponse.data}`); 
    } catch (err) {
        console.log(err);
    }
  });

// Forward state retrieval to Dapr state endpoint
app.get('/state', async (req, res) => {
  try {
    // Getting Dapr state
    const apiResponse = await axios.get(`${stateUrl}/votacionesState`);

    return res.send(apiResponse.data);
  } catch (err) {
    console.log(err);
  }
});

// Forward state persistence to Dapr state endpoint
app.post('/persist', async (req, res) => {
  try {
     // Saving Dapr state
    const apiResponse = await axios.post(stateUrl, req.body);
    return res.send(apiResponse.data);  
  } catch (err) {
    console.log(err);
  }
});

// Serve static files
app.use(express.static(path.join(__dirname, 'client/build')));

// For default home request route to React client
app.get('/', async function (_req, res) {
  try {
    return await res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
  } catch (err) {
    console.log(err);
  }
});

app.listen(process.env.PORT || port, () => console.log(`Listening on port ${port}!`));