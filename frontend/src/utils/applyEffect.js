import { gsap } from "gsap";

export default function applyEffect(el, effect, duration, currentText) {
  gsap.killTweensOf(el); // Reset any previous animations

  switch (effect) {
    case 'Fade':
      gsap.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.5 });
      gsap.to(el, { opacity: 0, delay: duration - 0.5, duration: 0.5 });
      break;

    case 'Slide In':
      gsap.fromTo(
        el,
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.5 }
      );
      gsap.to(el, {
        opacity: 0,
        y: 30,
        delay: duration - 0.5,
        duration: 0.5
      });
      break;

    case 'Scale':
      gsap.fromTo(
        el,
        { opacity: 0, scale: 0.5 },
        { opacity: 1, scale: 1, duration: 0.5 }
      );
      gsap.to(el, {
        opacity: 0,
        scale: 0.5,
        delay: duration - 0.5,
        duration: 0.5
      });
      break;

    case 'Typewriter':
      gsap.set(el, { opacity: 1 });
      el.innerText = '';
      const chars = currentText.split('');
      chars.forEach((char, index) => {
        setTimeout(() => {
          el.innerText += char;
        }, index * 40); // 25fps = 40ms per char
      });
      gsap.to(el, { opacity: 0, delay: duration, duration: 0.5 });
      break;
  }
};