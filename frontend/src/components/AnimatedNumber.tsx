import { useEffect, useState } from "react";

interface AnimatedNumberProps {
  value: string | number;
  duration?: number; // duration in ms
}

export default function AnimatedNumber({ value, duration = 2000 }: AnimatedNumberProps) {
  const [displayValue, setDisplayValue] = useState("");

  useEffect(() => {
    const cleanValue = String(value).replace(/,/g, "");
    const match = cleanValue.match(/^([^\d-]*)(-?\d+\.?\d*)(.*)$/);

    if (!match) {
      setDisplayValue(String(value));
      return;
    }

    const prefix = match[1];
    const targetNum = parseFloat(match[2]);
    const suffix = match[3];

    // Determine decimal places
    const decimalPlaces = match[2].includes(".")
      ? match[2].split(".")[1].length
      : 0;

    let startTimestamp: number | null = null;
    let animationFrameId: number;

    const step = (timestamp: number) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);

      // Easing function: easeOutExpo (starts fast, slows down smoothly)
      const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      const currentNum = targetNum * ease;

      // Format current number with the same decimal places
      let formattedNum = currentNum.toFixed(decimalPlaces);
      if (!match[2].includes(".")) {
        // Add commas to integers
        formattedNum = Math.floor(currentNum).toLocaleString();
      } else {
        // For floats, format the integer part with commas
        const parts = formattedNum.split(".");
        parts[0] = parseInt(parts[0], 10).toLocaleString();
        formattedNum = parts.join(".");
      }

      setDisplayValue(`${prefix}${formattedNum}${suffix}`);

      if (progress < 1) {
        animationFrameId = window.requestAnimationFrame(step);
      } else {
        // Set exact final value at the end of the animation
        let finalFormatted = targetNum.toFixed(decimalPlaces);
        if (!match[2].includes(".")) {
          finalFormatted = Math.floor(targetNum).toLocaleString();
        } else {
          const parts = finalFormatted.split(".");
          parts[0] = parseInt(parts[0], 10).toLocaleString();
          finalFormatted = parts.join(".");
        }
        setDisplayValue(`${prefix}${finalFormatted}${suffix}`);
      }
    };

    animationFrameId = window.requestAnimationFrame(step);

    return () => {
      window.cancelAnimationFrame(animationFrameId);
    };
  }, [value, duration]);

  return <>{displayValue}</>;
}
