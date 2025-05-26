import '../styles/PreviewVideo.css';
import { useEffect, useState, useRef } from 'react';
import applyEffect from '../utils/applyEffect';
import EditModal from './EditModal';

const data = {
  'video': 'https://res.cloudinary.com/dfa9owyll/video/upload/v1748136943/q4xi4jazlxvlsxirvfij.mp4', 
  'duration': '44.31', 
  'subtitles': [
    {'text': 'Mat trời ló dạng qua làn sương mỏng,', 'start': 0, 'end': 2.4}, 
    {'text': 'một bà cụ áo dài chậm rãi đẩy', 'start': 2.4, 'end': 4.8}, 
    {'text': 'xe qua cánh đồng lúa xanh mướt. Tiếng', 'start': 4.8, 'end': 7.2}, 
    {'text': 'cười trẻ con vang lên từ ngôi nhà', 'start': 7.2, 'end': 9.6}, 
    {'text': 'mái tranh, mùi khói bếp lan tỏa.', 'start': 9.6, 'end': 12.0}, 
    {'text': 'Phố cờ đỏ sao vàng rực rỡ,', 'start': 12.0, 'end': 14.2}, 
    {'text': 'tiếng rao hàng rong hòa cùng nhịp', 'start': 14.2, 'end': 16.4}, 
    {'text': 'xích lô. Bàn tay thoăn thoắt gói', 'start': 16.4, 'end': 18.59}, 
    {'text': 'bánh cuốn, giọt mắm cay nồng thấm', 'start': 18.59, 'end': 20.79}, 
    {'text': 'vào vị giác người lữ khách.', 'start': 20.79, 'end': 22.99}, 
    {'text': 'Chiều buông xuống bến sông Hồng, mái', 'start': 22.99, 'end': 25.27}, 
    {'text': 'chèo khua nước lấp lánh ánh vàng.', 'start': 25.27, 'end': 27.54}, 
    {'text': 'Câu hò "ơi à ơi..." vọng từ', 'start': 27.54, 'end': 29.82}, 
    {'text': 'con thuyền nan, đôi mắt người', 'start': 29.82, 'end': 32.09}, 
    {'text': 'chài lưới in bóng hoàng hôn.', 'start': 32.09, 'end': 34.37}, 
    {'text': 'Đêm thành phố thức giấc trong muôn ngàn', 'start': 34.37, 'end': 36.36}, 
    {'text': 'đèn hoa đăng. Bàn tay trẻ lau vội', 'start': 36.36, 'end': 38.35}, 
    {'text': 'mồ hôi, gõ phím máy tính bên', 'start': 38.35, 'end': 40.33}, 
    {'text': 'tách cà phê đen nóng hổi -', 'start': 40.33, 'end': 42.32}, 
    {'text': 'nhịp sống mới vẫn giữ hồn xưa.', 'start': 42.32, 'end': 44.31}]
};

const textEffects = ['Fade', 'Slide In', 'Scale', 'Typewriter'];
const stickerOptions = ['stickers/bear.png', 'stickers/bear.png'];

export default function PreviewVideo() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const subtitleRef = useRef(null);

  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedEffect, setSelectedEffect] = useState('Fade');
  const [currentText, setCurrentText] = useState('');

  const [isEditOpen, setIsEditOpen] = useState(false);


  useEffect(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const subtitleEl = subtitleRef.current;

    let animationFrameId;

    const render = () => {
      if (video.paused || video.ended) return;

      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const currentTime = video.currentTime;
      const subtitle = data.subtitles.find(
        (sub) => currentTime >= sub.start && currentTime <= sub.end
      );

      if (subtitle) {
        if (currentText !== subtitle.text) {
          setCurrentText(subtitle.text);
          subtitleEl.innerText = subtitle.text;
          subtitleEl.style.opacity = '1';

          applyEffect(subtitleEl, selectedEffect, subtitle.end - currentTime, currentText, video);
        }
      } else {
        subtitleEl.innerText = '';
        subtitleEl.style.opacity = '0';
      }

      animationFrameId = requestAnimationFrame(render);
    };

    if (isPlaying) {
      render();
    }

    return () => cancelAnimationFrame(animationFrameId);
  }, [isPlaying, selectedEffect, currentText]);


  const handlePlay = () => {
    videoRef.current?.play();
    setIsPlaying(true);
  };

  const handlePause = () => {
    videoRef.current?.pause();
    setIsPlaying(false);
  };

  const handleApplyTextEffect = (effect) => {
    setSelectedEffect(effect);
    playAgain();
  };

  const playAgain = () => {
    setCurrentText('');
    if (videoRef.current) {
      videoRef.current.currentTime = 0;
      videoRef.current.play();
      setIsPlaying(true);
    }
  }

  return (
    <div className='d-flex flex-column align-items-center justify-content-center text-white'>

      <div style={{ position: 'relative', width: 384, height: 512 }}>
        <canvas ref={canvasRef} width={384} height={512} style={{ border: '1px solid #444' }}/>

        <div ref={subtitleRef} className='subtitle'></div>

        <video
          ref={videoRef}
          src={data.video}
          style={{ display: 'none' }}
          onLoadedMetadata={() => setIsPlaying(false)}
        />
      </div>

      <div style={{ marginTop: '10px' }}>
        <button onClick={handlePlay}>Play</button>
        <button onClick={handlePause}>Pause</button>
      </div>

      <button className="edit-button p2" onClick={() => setIsEditOpen(true)}>
        Edit
      </button>

      {isEditOpen && (
        <EditModal
          onClose={() => setIsEditOpen(false)}
          onApplyTextEffect={handleApplyTextEffect}
        />
      )}
    </div>
  );
}