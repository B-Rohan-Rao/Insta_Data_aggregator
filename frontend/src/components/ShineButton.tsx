import React from "react";
import { cn } from "../lib/utils";

interface ShineButtonProps {
  label?: string;
  onClick?: () => void;
  className?: string;
  size?: "sm" | "md" | "lg";
  bgColor?: string; // Can be hex or gradient
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  children?: React.ReactNode;
}

const sizeStyles: Record<
  NonNullable<ShineButtonProps["size"]>,
  { padding: string; fontSize: string }
> = {
  sm: { padding: "0.5rem 1rem", fontSize: "0.875rem" },
  md: { padding: "0.6rem 1.4rem", fontSize: "1rem" },
  lg: { padding: "0.8rem 1.8rem", fontSize: "1.125rem" },
};

export const ShineButton: React.FC<ShineButtonProps> = ({
  label,
  onClick,
  className = "",
  size = "md",
  bgColor = "linear-gradient(325deg, hsl(217 100% 56%) 0%, hsl(194 100% 69%) 55%, hsl(217 100% 56%) 90%)",
  type = "button",
  disabled = false,
  children,
}) => {
  const { padding, fontSize } = sizeStyles[size];

  // Determine whether to use solid color or gradient
  const backgroundImage = bgColor.startsWith("linear-gradient")
    ? bgColor
    : `linear-gradient(to right, ${bgColor}, ${bgColor})`;

  const hasCustomPadding = className.includes("p-") || className.includes("px-") || className.includes("py-");
  const hasCustomFontSize = className.includes("text-");

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={cn(
        "group relative text-white font-medium rounded-md min-w-[120px] min-h-[44px] transition-all duration-700 ease-in-out overflow-hidden border-none cursor-pointer shadow-[0px_0px_20px_rgba(71,184,255,0.5),0px_5px_5px_-1px_rgba(58,125,233,0.25),inset_4px_4px_8px_rgba(175,230,255,0.5),inset_-4px_-4px_8px_rgba(19,95,216,0.35)] focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-blue-500 hover:bg-[length:280%_auto] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed",
        className
      )}
      style={{
        backgroundImage,
        backgroundSize: "280% auto",
        backgroundPosition: "initial",
        color: "hsl(0 0% 100%)",
        fontSize: hasCustomFontSize ? undefined : fontSize,
        padding: hasCustomPadding ? undefined : padding,
        transition: "0.8s",
      }}
      onMouseEnter={(e) => {
        if (!disabled) {
          (e.currentTarget as HTMLButtonElement).style.backgroundPosition = "right top";
        }
      }}
      onMouseLeave={(e) => {
        if (!disabled) {
          (e.currentTarget as HTMLButtonElement).style.backgroundPosition = "initial";
        }
      }}
    >
      <span className="relative z-10 flex items-center justify-center gap-2">
        {children || label || "Shine now"}
      </span>

      {/* Shine effect */}
      <div className="shine-effect" />
    </button>
  );
};
