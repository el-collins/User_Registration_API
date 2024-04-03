import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';

function App() {
  return (
    <Router>
      <p>hello</p>
      <div className="App">
        <Switch>
          <Route path="/register">
            <RegistrationForm />
          </Route>
          <Route path="/login">
            <LoginForm />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;