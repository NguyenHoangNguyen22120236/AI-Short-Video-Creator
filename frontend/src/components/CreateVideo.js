import '../styles/CreateVideo.css';
import { useState } from 'react';

export default function CreateVideo() {
    const [topic, setTopic] = useState('');
    const [language, setLanguage] = useState('English');

    return (
        <div className="container px-lg-5 py-lg-3 px-md-3 py-md-2 px-sm-1 py-sm-1 text-white">
            <div className="input-box mx-lg-5 mt-lg-5 mx-md-3 mt-md-3 mx-sm-3 mt-sm-1 mt-3 mx-1">
                <textarea
                    placeholder="Give me a topic in English or Vietnamese"
                    maxLength={100}
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                />
                <div className="d-flex justify-content-between align-items-center flex-lg-row flex-md-row flex-sm-column flex-column">
                    <span className="char-limit">{topic.length} / 100</span>
                    <div className='d-flex gap-5 align-items-center'>
                        <button className="btn">Suggest Trendy Topics</button>
                        <button className="btn btn-primary">Generate Video</button>
                    </div>
                </div>
            </div>
        </div>
    )
}