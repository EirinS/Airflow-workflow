import './App.css';
import Form from "@rjsf/material-ui";
import { schema, uiSchema } from './Schemas'
import React, { useState } from 'react';

function App() {
  const [workflowStatus, setWorkflowStatus] = useState("Workflow not submitted")

  const api_url = "api/v1/"
  const dag_id = "ArcticOcean"

  /*
  const saveParameters = (event) => {
    console.log(event);
    const fileData = JSON.stringify(event.formData);
    const blob = new Blob([fileData], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = 'ap_params.json';
    link.href = url;
    link.click();
  }

  const getDags = () => {
    return fetch(api_url + 'dags?limit=100', {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      }
    })
      .then((response) => {
        console.log("success:");
      })
      .catch((error) => {
        console.error(error);
      });
  }*/

  const runDag = (event) => {
    return fetch(api_url + 'dags/' + dag_id + '/dagRuns', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        conf: event.formData
      })
    })
      .then(res => res.json())
      .then((json) => {
        console.log(json)
        setWorkflowStatus("Workflow with id: " + json.dag_run_id + " submitted");
      })
      .catch((error) => {
        console.log(error)
      });
  };

  const airflowStyle = {
    marginTop: "15px",
    fontSize: "20px",
  }

  const line = {
    margin: "15px 0",
    width: "100%",
    color: "black",
  }

  return (
    <div className="App">
      <div>
        <Form schema={schema}
          uiSchema={uiSchema}
          onSubmit={runDag} />
      </div>
      <hr style={line}></hr>
      <div>{workflowStatus}</div>
      <div className="AirflowStatus" style={airflowStyle}>
        <a href={"http://localhost:8080/tree?dag_id=" + dag_id}>Click here to se the workflow run status</a>
      </div>
    </div>
  );
}

export default App;
