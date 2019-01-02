import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Chats from './Chats';
import Header from './Header';
import Login from './Login';

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <Header />
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
