import '../styles/Header.css';

export default function Header() {
    return(
        <div className="d-flex justify-content-between align-items-center header">
            <div className="d-flex gap-3 align-items-center">
                <img src="/logo.png" alt="logo" className="logo"/>
                <h1 className="text-center text-white fs-4">AI Short Video Creator</h1>
            </div>
            <div className='user d-flex justify-content-center align-items-center gap-2'>
                <img src="/user.png" alt="account"/>
            </div>
        </div>
    )
}