import AuthForm from './AuthForm';
import "../styles/LoginSignUp.css";

export default function LoginSignUp() {
    return (
        <div className="d-flex justify-content-center align-items-center vh-100 bg-dark">
            <div className="text-center p-4" style={{ maxWidth: '600px' }}>
                {/* Logo + App Title */}
                <div className="d-flex align-items-center mb-3 text-white">
                    <img
                        src="/logo.png" // Replace with your actual logo path
                        alt="Logo"
                        style={{ width: '30px', height: '30px', marginRight: '10px' }}
                    />
                    <span className="fw-bold fs-5">AI Short Video Creator</span>
                </div>

                {/* Main Heading with Gradient */}
                <h3 className="fw-bold mb-4 text-white">
                    Welcome to{' '}
                    <span className="text-gradient">AI Short Video Creator</span>
                </h3>

                {/* Auth Form */}
                <AuthForm />
            </div>
        </div>
    );
}
