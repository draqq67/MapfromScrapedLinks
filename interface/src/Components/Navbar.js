import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

function PageNavbar() {
return (
    <Navbar expand="lg" className="bg-body-tertiary" >
        <Container style={{ margin: '0', marginBottom: '10px' }}>
            <Navbar.Brand href="#home">Project</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    <Nav.Link href="/">Home</Nav.Link>
                    <Nav.Link href="/map">Map</Nav.Link>
                    <Nav.Link href='/statistics'>Statistics</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Container>
    </Navbar>
);
}

export default PageNavbar;