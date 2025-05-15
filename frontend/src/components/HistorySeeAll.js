import '../styles/HistorySeeAll.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faClock } from '@fortawesome/free-solid-svg-icons';
import { format, parseISO } from 'date-fns';
import { Link } from 'react-router-dom';

const historyData = {
  "Tue May 06 2025": [
    { id: 1, topic: 'Python', time: '2025-05-06 13:20:56.789012+00:00' },
    { id: 2, topic: 'Python', time: '2025-05-06 13:20:56.789012+00:00' }
  ],
  "Mon May 05 2025": [
    { id: 3, topic: 'Python', time: '2025-05-06 13:20:56.789012+00:00' },
    { id: 4, topic: 'Python', time: '2025-05-06 13:20:56.789012+00:00' }
  ]
};

export default function HistorySeeAll() {
    return (
        <div className='container px-lg-5 py-lg-3 px-md-3 py-md-2 px-sm-1 py-sm-1 text-white'>
            <div className='d-flex justify-content-start gap-5 p-0 flex-column'>
                <div className="history-header d-flex justify-content-between align-items-center p-3">
                    <h2>History</h2>
                    <Link to ="/create-video" className="text-decoration-none">
                        <button className="create-button p-2">Create new <FontAwesomeIcon icon={faPlus} /></button>
                    </Link>
                </div>
                
                {Object.entries(historyData).map(([date, videos]) => (
                    <div key={date} className="d-flex flex-column gap-3 p-0 mt-2">    
                         <h4 className="date-label mb-3">{date}</h4>
                         {videos.map((video) => (
                            <div key={video.id} className="history-card d-flex justify-content-between align-items-center p-3">
                                <div className='d-flex align-items-center flex-column'>
                                    <div className='d-flex gap-3 align-items-center fs-5'>
                                        <FontAwesomeIcon icon={faClock}/>
                                        <h4>{video.topic}</h4>
                                    </div>
                                    <p className='m-0'>Created at: {format(parseISO(video.time), 'HH:mm')}</p>
                                </div>
                                <div className="dots">⋮</div>
                            </div>
                         ))}
                    </div>
                ))}
            </div>
        </div>
    )
}