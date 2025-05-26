import { gsap } from "gsap";

let effectTimeline = null;

export default function applyEffect(el, effect, duration, currentText, video) {
  gsap.killTweensOf(el); // Reset any previous animations
  if (effectTimeline) {
    effectTimeline.kill();
    effectTimeline = null;
  }

  // Remove previous listeners to avoid stacking
  video.onpause = null;
  video.onplay = null;

  switch (effect) {
    case 'Fade':
      effectTimeline = gsap.timeline();
      effectTimeline.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.5 });
      effectTimeline.to(el, { opacity: 0, duration: 0.5 }, duration - 0.5);
      break;

    case 'Slide In':
      effectTimeline = gsap.timeline();
      effectTimeline.fromTo(el, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 });
      effectTimeline.to(el, { opacity: 0, y: 30, duration: 0.5 }, duration - 0.5);
      break;

    case 'Scale':
      effectTimeline = gsap.timeline();
      effectTimeline.fromTo(el, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.5 });
      effectTimeline.to(el, { opacity: 0, scale: 0.5, duration: 0.5 }, duration - 0.5);
      break;

    case 'Typewriter':
      effectTimeline = gsap.timeline();
      gsap.set(el, { opacity: 1 });
      el.innerText = '';
      const chars = currentText.split('');
      chars.forEach((char, index) => {
        effectTimeline.call(() => {
          el.innerText += char;
        }, null, index * 0.04); // 40ms per char
      });
      effectTimeline.to(el, { opacity: 0, duration: 0.5 }, duration);
      break;
  }

  // Pause/resume timeline with video
  video.onpause = () => {
    if (effectTimeline) effectTimeline.pause();
  };
  video.onplay = () => {
    if (effectTimeline) effectTimeline.resume();
  };
}