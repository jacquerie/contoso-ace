import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Chats from './Chats';
import Login from './Login';

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <h1>Contoso ACE</h1>
        <Router>
          <div className="Router">
            <Route path="/" exact component={Login} />
            <Route path="/chats" component={Chats} />
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
