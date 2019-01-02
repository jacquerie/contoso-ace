import React from 'react';
import { Container, Nav, NavItem, NavLink, Navbar } from 'reactstrap';

import './Header.css';

class Header extends React.Component {
  render() {
    return (
      <div className="Header">
        <Navbar dark color="primary" expand="xs">
          <Container>
            <h1 className="navbar-text">Contoso ACE</h1>
            <Nav navbar>
              <NavItem className="navbar-text mr-3">Hello, Barbara!</NavItem>
              <NavItem>
                <NavLink href="#">Sign Out</NavLink>
              </NavItem>
            </Nav>
          </Container>
        </Navbar>
      </div>
    );
  }
}

export default Header;
