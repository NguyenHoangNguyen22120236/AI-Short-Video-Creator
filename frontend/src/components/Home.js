import React from 'react';
import '../styles/Home.css';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight, faClock } from '@fortawesome/free-solid-svg-icons';

export default function Home() {
    const navigate = useNavigate();

    const historyItems = [
        { id: 1, title: "Python", date: "6 days ago", image: "https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png" },
        { id: 2, title: "Python", date: "6 days ago", image: "https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png" },
        { id: 3, title: "Python", date: "6 days ago", image: "https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png" },
        { id: 4, title: "Python", date: "6 days ago", image: "https://i.postimg.cc/zXgFtzZ5/Deep-Focus-Music-To-Improve-Concentration-12-Hours-of-Ambient-Study-Music-to-Concentrate-576-Yo.png" },

    ];

    const handleCreateClick = () => {
        navigate('/create'); // Navigate to the AI video creation page
    };

    return (
        <div className='container p-1'>
            <div className='row p-3'>
                <div className='create-button col-lg-4 col-md-6 col-sm-10 col-10 d-flex justify-content-between align-items-center'>
                    <div className=' d-flex flex-column justify-content-around align-items-center'>
                        <span className='main-text'>Create AI Video</span>
                        <span className='extra-text'>Start from scratch</span>
                    </div>
                    <FontAwesomeIcon className='text-white' icon={faArrowRight} />
                </div>
            </div>
            <div className='row p-3'>
                <div className='d-flex justify-content-start align-items-center gap-3 p-0'>
                    <h2 className='main-text'>History</h2>
                    <a href="/history" className="see-all">See all</a>
                </div>
                <div className="d-flex flex-wrap justify-content-between align-items-center p-0">
                    {historyItems.map((item) => (
                        <div className='col-lg-4 col-md-6 col-sm-6 col-6 p-lg-5 p-md-3 p-sm-3 p-2' key={item.id}>
                            <div className='card'>
                                <img src={item.image} alt={item.title} className="thumbnail" />
                                <div className='d-flex justify-content-between align-items-center p-3'>
                                    <div>
                                        <div className="d-flex gap-3 align-items-center fs-5">
                                            <FontAwesomeIcon icon={faClock} className=''/>
                                            <h4>{item.title}</h4>
                                        </div>
                                        <h5>{item.date}</h5>
                                    </div>
                                    <div className="dots">⋮</div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}