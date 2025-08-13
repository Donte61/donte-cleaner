"""
Modern UI Components for DonTe Cleaner v3.0
Advanced Technological Design with Dark Theme and Animations
"""

import tkinter as tk
from tkinter import ttk
import math
import threading
import time
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

class ModernFrame(ttk.Frame):
    """Modern frame with gradient background and rounded corners"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(style="Modern.TFrame")

class GradientFrame(tk.Canvas):
    """Frame with gradient background"""
    
    def __init__(self, parent, color1="#1a1a2e", color2="#16213e", **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind('<Configure>', self.draw_gradient)
        
    def draw_gradient(self, event=None):
        """Draw gradient background"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        # Create gradient
        for i in range(height):
            ratio = i / height
            r1, g1, b1 = self.hex_to_rgb(self.color1)
            r2, g2, b2 = self.hex_to_rgb(self.color2)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.create_line(0, i, width, i, fill=color, tags="gradient")
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class AnimatedButton(tk.Canvas):
    """Modern animated button with hover effects"""
    
    def __init__(self, parent, text="", command=None, 
                 bg_color="#0066cc", hover_color="#0080ff", 
                 text_color="white", width=200, height=50, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, **kwargs)
        
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.width = width
        self.height = height
        self.is_hovered = False
        self.animation_running = False
        
        self.configure(bg=bg_color)
        self.draw_button()
        self.bind_events()
    
    def draw_button(self):
        """Draw the button"""
        self.delete("all")
        
        # Background with rounded corners
        color = self.hover_color if self.is_hovered else self.bg_color
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 
                                radius=15, fill=color, outline="")
        
        # Text
        self.create_text(self.width//2, self.height//2, 
                        text=self.text, fill=self.text_color,
                        font=("Segoe UI", 11, "bold"))
        
        # Glow effect when hovered
        if self.is_hovered:
            self.create_rounded_rect(0, 0, self.width, self.height, 
                                    radius=17, fill="", outline=self.hover_color, 
                                    width=2)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=15, **kwargs):
        """Create rounded rectangle"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def bind_events(self):
        """Bind mouse events"""
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
    
    def on_enter(self, event):
        """Mouse enter event"""
        self.is_hovered = True
        self.animate_hover()
    
    def on_leave(self, event):
        """Mouse leave event"""
        self.is_hovered = False
        self.animate_hover()
    
    def on_click(self, event):
        """Mouse click event"""
        if self.command:
            self.command()
        self.animate_click()
    
    def animate_hover(self):
        """Animate hover effect"""
        if self.animation_running:
            return
        
        self.animation_running = True
        # Use safe threading approach
        self.after_idle(self.draw_button)
        self.after(100, lambda: setattr(self, 'animation_running', False))
    
    def _hover_animation(self):
        """Hover animation thread - DEPRECATED, use animate_hover instead"""
        # Removed to prevent thread issues
        pass
    
    def animate_click(self):
        """Animate click effect"""
        original_width = self.width
        original_height = self.height
        
        # Shrink
        for i in range(5):
            scale = 1 - (i * 0.02)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            self.configure(width=new_width, height=new_height)
            self.update()
            time.sleep(0.01)
        
        # Restore
        for i in range(5):
            scale = 0.9 + (i * 0.02)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            self.configure(width=new_width, height=new_height)
            self.update()
            time.sleep(0.01)

class NeonProgressBar(tk.Canvas):
    """Neon-style progress bar with glow effects"""
    
    def __init__(self, parent, width=300, height=30, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg="#1a1a2e", **kwargs)
        
        self.width = width
        self.height = height
        self.progress = 0
        self.max_value = 100
        self.bar_color = "#00ffff"
        self.bg_color = "#333366"
        self.glow_color = "#66ffff"
        
        self.draw_background()
    
    def draw_background(self):
        """Draw progress bar background"""
        self.delete("bg")
        
        # Background track
        self.create_rounded_rect(5, 5, self.width-5, self.height-5,
                                radius=self.height//2, fill=self.bg_color,
                                outline="#555577", tags="bg")
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=15, **kwargs):
        """Create rounded rectangle"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def set_progress(self, value):
        """Set progress value (0-100)"""
        try:
            self.progress = max(0, min(100, value))
            self.draw_progress()
            self.update_idletasks()  # Safer update
        except tk.TclError:
            # Widget was destroyed, ignore update
            pass
    
    def draw_progress(self):
        """Draw progress bar"""
        try:
            self.delete("progress")
        except tk.TclError:
            # Widget was destroyed, ignore drawing
            return
        
        if self.progress > 0:
            # Calculate progress width
            progress_width = ((self.width - 10) * self.progress) / 100
            
            # Glow effect (multiple layers)
            for i in range(3):
                glow_width = progress_width + (i * 2)
                alpha = 1 - (i * 0.3)
                glow_color = self.adjust_color_alpha(self.glow_color, alpha)
                
                if glow_width > 0:
                    self.create_rounded_rect(5 - i, 5 - i, 5 + glow_width + i, 
                                           self.height - 5 + i,
                                           radius=self.height//2, 
                                           fill=glow_color, outline="",
                                           tags="progress")
            
            # Main progress bar
            if progress_width > 0:
                self.create_rounded_rect(5, 5, 5 + progress_width, self.height - 5,
                                       radius=self.height//2, fill=self.bar_color,
                                       outline="", tags="progress")
                
                # Highlight
                highlight_width = progress_width * 0.8
                if highlight_width > 0:
                    self.create_rounded_rect(7, 7, 7 + highlight_width, self.height//2,
                                           radius=self.height//4, fill="#ffffff",
                                           outline="", tags="progress")
    
    def adjust_color_alpha(self, color, alpha):
        """Adjust color transparency (simulated)"""
        # Simple alpha simulation by blending with background
        return color  # Simplified for now

class HolographicCard(tk.Canvas):
    """Holographic-style card with animated borders"""
    
    def __init__(self, parent, width=300, height=200, title="", **kwargs):
        super().__init__(parent, width=width, height=height,
                        highlightthickness=0, bg="#1a1a2e", **kwargs)
        
        self.width = width
        self.height = height
        self.title = title
        self.border_colors = ["#ff0080", "#8000ff", "#0080ff", "#00ff80", "#ff8000"]
        self.current_color = 0
        self.animation_active = True
        
        self.draw_card()
        self.start_animation()
    
    def draw_card(self):
        """Draw holographic card"""
        self.delete("card")
        
        # Background
        self.create_rounded_rect(10, 10, self.width-10, self.height-10,
                                radius=20, fill="#2a2a4e", outline="",
                                tags="card")
        
        # Animated border
        border_color = self.border_colors[self.current_color]
        self.create_rounded_rect(8, 8, self.width-8, self.height-8,
                                radius=22, fill="", outline=border_color,
                                width=3, tags="card")
        
        # Inner glow
        self.create_rounded_rect(12, 12, self.width-12, self.height-12,
                                radius=18, fill="", outline=border_color,
                                width=1, tags="card")
        
        # Title
        if self.title:
            self.create_text(self.width//2, 30, text=self.title,
                           fill="white", font=("Segoe UI", 14, "bold"),
                           tags="card")
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=15, **kwargs):
        """Create rounded rectangle"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def start_animation(self):
        """Start border animation"""
        if self.animation_active:
            self.animate_border()
    
    def animate_border(self):
        """Animate border colors"""
        def update_color():
            if self.animation_active:
                try:
                    self.current_color = (self.current_color + 1) % len(self.border_colors)
                    self.draw_card()
                    self.after(500, update_color)
                except tk.TclError:
                    # Widget was destroyed, stop animation
                    self.animation_active = False
        
        update_color()
    
    def stop_animation(self):
        """Stop border animation"""
        self.animation_active = False

class ParticleSystem:
    """Particle system for visual effects"""
    
    def __init__(self, canvas, num_particles=50):
        self.canvas = canvas
        self.particles = []
        self.num_particles = num_particles
        self.active = True
        
        self.init_particles()
        self.animate()
    
    def init_particles(self):
        """Initialize particles"""
        import random
        
        width = 1400  # Default canvas width
        height = 900  # Default canvas height
        
        for _ in range(self.num_particles):
            particle = {
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'size': random.randint(1, 3),
                'color': random.choice(['#00ffff', '#ff00ff', '#ffff00', '#00ff00'])
            }
            self.particles.append(particle)
    
    def animate(self):
        """Animate particles"""
        if not self.active:
            return
        
        try:
            self.canvas.delete("particle")
            width = self.canvas.winfo_width() or 1400
            height = self.canvas.winfo_height() or 900
            
            for particle in self.particles:
                # Update position
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                
                # Wrap around edges
                if particle['x'] < 0:
                    particle['x'] = width
                elif particle['x'] > width:
                    particle['x'] = 0
                
                if particle['y'] < 0:
                    particle['y'] = height
                elif particle['y'] > height:
                    particle['y'] = 0
                
                # Draw particle
                self.canvas.create_oval(
                    particle['x'], particle['y'],
                    particle['x'] + particle['size'], 
                    particle['y'] + particle['size'],
                    fill=particle['color'], outline="",
                    tags="particle"
                )
            
            # Schedule next frame
            self.canvas.after(50, self.animate)
        except tk.TclError:
            # Canvas was destroyed, stop animation
            self.active = False
    
    def stop(self):
        """Stop particle animation"""
        self.active = False

class ModernTab(ttk.Frame):
    """Modern tab with enhanced styling"""
    
    def __init__(self, parent, title="", icon="", **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        self.icon = icon
        self.configure(style="ModernTab.TFrame")
        
        self.create_content()
    
    def create_content(self):
        """Create tab content"""
        # Header
        header_frame = tk.Frame(self, bg="#2a2a4e", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_label = tk.Label(header_frame, 
                              text=f"{self.icon} {self.title}",
                              font=("Segoe UI", 16, "bold"),
                              fg="white", bg="#2a2a4e")
        title_label.pack(side="left", padx=20, pady=15)
        
        # Content area
        self.content_frame = tk.Frame(self, bg="#1a1a2e")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

class StatusIndicator(tk.Canvas):
    """Modern status indicator with pulse animation"""
    
    def __init__(self, parent, status="inactive", size=20, **kwargs):
        super().__init__(parent, width=size, height=size,
                        highlightthickness=0, bg="#1a1a2e", **kwargs)
        
        self.size = size
        self.status = status
        self.pulse_size = size // 2
        self.max_pulse = size - 2
        self.pulse_direction = 1
        
        self.status_colors = {
            'active': '#00ff00',
            'warning': '#ffff00', 
            'error': '#ff0000',
            'inactive': '#666666'
        }
        
        self.draw_indicator()
        self.start_pulse()
    
    def draw_indicator(self):
        """Draw status indicator"""
        self.delete("all")
        
        color = self.status_colors.get(self.status, '#666666')
        center = self.size // 2
        
        # Outer pulse (for active status)
        if self.status == 'active':
            self.create_oval(center - self.pulse_size, center - self.pulse_size,
                           center + self.pulse_size, center + self.pulse_size,
                           fill="", outline=color, width=2)
        
        # Main indicator
        radius = min(6, self.size // 3)
        self.create_oval(center - radius, center - radius,
                        center + radius, center + radius,
                        fill=color, outline="")
    
    def start_pulse(self):
        """Start pulse animation for active status"""
        def pulse():
            try:
                if self.status == 'active':
                    self.pulse_size += self.pulse_direction
                    if self.pulse_size >= self.max_pulse or self.pulse_size <= self.size // 4:
                        self.pulse_direction *= -1
                    
                    self.draw_indicator()
                
                self.after(100, pulse)
            except tk.TclError:
                # Widget was destroyed, stop animation
                pass
        
        pulse()
    
    def set_status(self, status):
        """Set indicator status"""
        self.status = status
        self.draw_indicator()

class TechWidget(tk.Frame):
    """Base class for technological widgets"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#1a1a2e", **kwargs)
        self.setup_style()
    
    def setup_style(self):
        """Setup technological styling"""
        self.configure(relief="flat", bd=0)
