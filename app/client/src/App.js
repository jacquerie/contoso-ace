import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Chats from './Chats';
import Header from './Header';
import Login from './Login';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      employee: null,
    };

    this.loginEmployee = this.loginEmployee.bind(this);
    this.logoutEmployee = this.logoutEmployee.bind(this);
  }

  componentDidMount() {
    this.fetchEmployee();
  }

  fetchEmployee() {
    return fetch('/api/employees/current', {
      method: 'GET',
      credentials: 'same-origin',
    })
      .then(response => (response.ok ? response.json() : null))
      .then(json => this.setState({ employee: json }));
  }

  loginEmployee(email, password) {
    return fetch('/api/employees/login', {
      method: 'POST',
      credentials: 'same-origin',
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    }).then(response => {
      if (response.ok) {
        this.fetchEmployee();
      }
    });
  }

  logoutEmployee() {
    return fetch('/api/employees/logout', {
      method: 'POST',
      credentials: 'same-origin',
    })
      .then(response => (response.ok ? null : this.state.employee))
      .then(json => this.setState({ employee: json }));
  }

  render() {
    return (
      <div className="App">
        <Router>
          <div className="Router">
            <Header
              employee={this.state.employee}
              logoutEmployee={this.logoutEmployee}
            />
            <Route
              path="/"
              exact
              render={props => (
                <Login {...props} loginEmployee={this.loginEmployee} />
              )}
            />
            <Route path="/chats" component={Chats} />
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
