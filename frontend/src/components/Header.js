import '../styles/Header.css';
import { Link } from 'react-router-dom';

export default function Header() {
    return(
        <div className="d-flex justify-content-between align-items-center header">
            <div className="d-flex gap-3 align-items-center">
                <img src="/logo.png" alt="logo" className="logo"/>
                <Link to="/" className="text-decoration-none">
                    <h1 className="text-center text-white fs-4">AI Short Video Creator</h1>
                </Link>
            </div>
            <div className='user d-flex justify-content-center align-items-center gap-2'>
                <img src="/user.png" alt="account"/>
            </div>
        </div>
    )
}