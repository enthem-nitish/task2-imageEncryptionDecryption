import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
import os
from tkinter import filedialog, messagebox
import threading
import random

# Set theme and appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ImageEncryptionApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🔐 Pixel Encryption Tool - Nitish Sharma")
        self.window.geometry("1100x750")
        self.window.resizable(False, False)
        
        # Variables
        self.original_image = None
        self.processed_image = None
        self.original_image_path = None
        self.current_method = "xor"
        self.key_value = 42
        
        # Initialize status label first
        self.status_label = None
        self.info_label = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, pady=10)
        
        # Left Panel - Controls
        self.create_left_panel()
        
        # Right Panel - Image Preview
        self.create_right_panel()
        
        # Status Bar - Create after other components
        self.create_status_bar()
        
    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, height=60, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="🔐 Pixel Encryption Tool",
            font=("Arial", 28, "bold"),
            text_color="#378ADD"
        )
        title.pack(side="left", padx=10)
        
        dev_label = ctk.CTkLabel(
            header_frame,
            text="👨‍💻 Developed by Nitish Sharma",
            font=("Arial", 14),
            text_color="#888888"
        )
        dev_label.pack(side="right", padx=10)
        
    def create_left_panel(self):
        left_frame = ctk.CTkFrame(self.content_frame, width=350, corner_radius=10)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Upload Section
        upload_frame = ctk.CTkFrame(left_frame, corner_radius=10)
        upload_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(
            upload_frame,
            text="📤 Upload Image",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 5))
        
        self.upload_btn = ctk.CTkButton(
            upload_frame,
            text="Choose Image",
            command=self.upload_image,
            height=40,
            font=("Arial", 14)
        )
        self.upload_btn.pack(pady=5, padx=20, fill="x")
        
        self.file_label = ctk.CTkLabel(
            upload_frame,
            text="No image selected",
            font=("Arial", 12),
            text_color="#888888"
        )
        self.file_label.pack(pady=5)
        
        # Key Section
        key_frame = ctk.CTkFrame(left_frame, corner_radius=10)
        key_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(
            key_frame,
            text="🔑 Encryption Key",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 5))
        
        key_input_frame = ctk.CTkFrame(key_frame, fg_color="transparent")
        key_input_frame.pack(pady=5, padx=20)
        
        self.key_entry = ctk.CTkEntry(
            key_input_frame,
            width=150,
            placeholder_text="Enter key (1-9999)",
            font=("Arial", 14)
        )
        self.key_entry.pack(side="left", padx=(0, 10))
        self.key_entry.insert(0, "42")
        
        random_btn = ctk.CTkButton(
            key_input_frame,
            text="🎲 Random",
            command=self.generate_random_key,
            width=80,
            height=32,
            font=("Arial", 12)
        )
        random_btn.pack(side="left")
        
        # Algorithm Section
        algo_frame = ctk.CTkFrame(left_frame, corner_radius=10)
        algo_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(
            algo_frame,
            text="⚙️ Algorithm",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 5))
        
        algorithms = [
            ("XOR Cipher", "xor"),
            ("Pixel Shift", "shift"),
            ("Channel Swap", "swap"),
            ("Invert + Key", "invert"),
            ("Row Shuffle", "shuffle"),
            ("Multi-layer", "multi")
        ]
        
        self.algo_buttons = {}
        algo_grid = ctk.CTkFrame(algo_frame, fg_color="transparent")
        algo_grid.pack(pady=5, padx=10, fill="x")
        
        for i, (name, value) in enumerate(algorithms):
            row = i // 2
            col = i % 2
            btn = ctk.CTkButton(
                algo_grid,
                text=name,
                command=lambda v=value: self.select_algorithm(v),
                height=35,
                font=("Arial", 12),
                fg_color="#2a2a2a",
                hover_color="#378ADD"
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            self.algo_buttons[value] = btn
        
        # Select first algorithm by default (status_label will be set later)
        for key, btn in self.algo_buttons.items():
            if key == "xor":
                btn.configure(fg_color="#378ADD")
            else:
                btn.configure(fg_color="#2a2a2a")
        
        # Action Buttons
        action_frame = ctk.CTkFrame(left_frame, corner_radius=10)
        action_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(
            action_frame,
            text="🔄 Actions",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 5))
        
        action_grid = ctk.CTkFrame(action_frame, fg_color="transparent")
        action_grid.pack(pady=5, padx=10, fill="x")
        
        self.encrypt_btn = ctk.CTkButton(
            action_grid,
            text="🔒 Encrypt",
            command=lambda: self.process_image("encrypt"),
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#378ADD",
            hover_color="#2a6db5"
        )
        self.encrypt_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.encrypt_btn.configure(state="disabled")
        
        self.decrypt_btn = ctk.CTkButton(
            action_grid,
            text="🔓 Decrypt",
            command=lambda: self.process_image("decrypt"),
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.decrypt_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.decrypt_btn.configure(state="disabled")
        
        # Progress Bar
        self.progress_frame = ctk.CTkFrame(left_frame, corner_radius=10)
        self.progress_frame.pack(fill="x", pady=5, padx=10)
        self.progress_frame.pack_forget()
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Processing...",
            font=("Arial", 12)
        )
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=300,
            height=10
        )
        self.progress_bar.pack(pady=5, padx=20)
        self.progress_bar.set(0)
        
        # Download Button
        self.download_btn = ctk.CTkButton(
            left_frame,
            text="💾 Download Result",
            command=self.download_result,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#FF9800",
            hover_color="#e68900"
        )
        self.download_btn.pack(pady=10, padx=20, fill="x")
        self.download_btn.pack_forget()
        
    def create_right_panel(self):
        right_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Original Image
        orig_frame = ctk.CTkFrame(right_frame, corner_radius=10)
        orig_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(
            orig_frame,
            text="📷 Original Image",
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
        self.orig_canvas = ctk.CTkLabel(
            orig_frame,
            text="No image loaded",
            font=("Arial", 14),
            text_color="#666666",
            width=300,
            height=300
        )
        self.orig_canvas.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Processed Image
        proc_frame = ctk.CTkFrame(right_frame, corner_radius=10)
        proc_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(
            proc_frame,
            text="✨ Processed Image",
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
        self.proc_canvas = ctk.CTkLabel(
            proc_frame,
            text="Run encryption/decryption",
            font=("Arial", 14),
            text_color="#666666",
            width=300,
            height=300
        )
        self.proc_canvas.pack(pady=10, padx=10, fill="both", expand=True)
        
    def create_status_bar(self):
        self.status_frame = ctk.CTkFrame(self.main_frame, height=30, fg_color="transparent")
        self.status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="✅ Ready",
            font=("Arial", 12),
            text_color="#888888"
        )
        self.status_label.pack(side="left", padx=10)
        
        self.info_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=("Arial", 12),
            text_color="#378ADD"
        )
        self.info_label.pack(side="right", padx=10)
        
    # ============== Core Functions ==============
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.original_image_path = file_path
                self.original_image = Image.open(file_path)
                
                # Display original image
                self.display_image(self.original_image, self.orig_canvas)
                
                # Update file label
                filename = os.path.basename(file_path)
                self.file_label.configure(text=f"📄 {filename}")
                if self.status_label:
                    self.status_label.configure(text="✅ Image loaded successfully")
                
                # Reset processed image
                self.processed_image = None
                self.proc_canvas.configure(image=None, text="Run encryption/decryption")
                self.download_btn.pack_forget()
                
                # Enable buttons
                self.encrypt_btn.configure(state="normal")
                self.decrypt_btn.configure(state="normal")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                
    def display_image(self, img, canvas, max_size=(350, 350)):
        """Display image on canvas with proper sizing"""
        if img is None:
            canvas.configure(image=None, text="No image")
            return
            
        # Resize image to fit canvas
        img_copy = img.copy()
        img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(img_copy)
        canvas.configure(image=photo, text="")
        canvas.image = photo  # Keep reference
        
    def select_algorithm(self, method):
        self.current_method = method
        # Update button colors
        for key, btn in self.algo_buttons.items():
            if key == method:
                btn.configure(fg_color="#378ADD")
            else:
                btn.configure(fg_color="#2a2a2a")
        if self.status_label:
            self.status_label.configure(text=f"✅ Selected: {method.upper()}")
        
    def generate_random_key(self):
        self.key_value = random.randint(1, 9999)
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, str(self.key_value))
        if self.status_label:
            self.status_label.configure(text=f"🎲 Random key generated: {self.key_value}")
        
    def get_key(self):
        try:
            key = int(self.key_entry.get())
            if 1 <= key <= 9999:
                return key
            else:
                messagebox.showwarning("Warning", "Key must be between 1 and 9999")
                return 42
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid integer key")
            return 42
            
    def process_image(self, operation):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return
            
        # Show progress
        self.progress_frame.pack(fill="x", pady=5, padx=10)
        self.progress_bar.set(0)
        self.progress_label.configure(text=f"{operation.capitalize()}ing...")
        
        # Disable buttons during processing
        self.encrypt_btn.configure(state="disabled")
        self.decrypt_btn.configure(state="disabled")
        
        # Process in separate thread
        def process():
            try:
                key = self.get_key()
                method = self.current_method
                
                # Convert PIL to numpy array
                img_array = np.array(self.original_image)
                if len(img_array.shape) == 3 and img_array.shape[2] == 4:  # Remove alpha channel
                    img_array = img_array[:, :, :3]
                
                # Update progress
                self.update_progress(0.2, "Converting pixels...")
                
                # Apply algorithm
                result = self.apply_algorithm(img_array, key, operation, method)
                
                # Update progress
                self.update_progress(0.8, "Rendering result...")
                
                # Convert back to PIL
                self.processed_image = Image.fromarray(result.astype('uint8'))
                
                # Display result
                self.window.after(0, lambda: self.display_image(
                    self.processed_image, 
                    self.proc_canvas
                ))
                
                # Update UI
                self.window.after(0, lambda: self.update_after_processing(
                    operation, key, method
                ))
                
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror(
                    "Error", f"Processing failed: {str(e)}"
                ))
                self.window.after(0, lambda: self.progress_frame.pack_forget())
                
            finally:
                self.window.after(0, lambda: self.encrypt_btn.configure(state="normal"))
                self.window.after(0, lambda: self.decrypt_btn.configure(state="normal"))
                
        threading.Thread(target=process, daemon=True).start()
        
    def apply_algorithm(self, img, key, operation, method):
        """Apply encryption/decryption algorithm"""
        h, w = img.shape[:2]
        result = img.copy()
        
        if method == "xor":
            k = key & 0xFF
            for i in range(h):
                for j in range(w):
                    result[i, j, 0] ^= k
                    result[i, j, 1] ^= (k ^ 0x5A)
                    result[i, j, 2] ^= (k ^ 0xA5)
                    
        elif method == "shift":
            k = key % 256
            direction = 1 if operation == "encrypt" else -1
            for i in range(h):
                for j in range(w):
                    result[i, j, 0] = (result[i, j, 0] + direction * k) % 256
                    result[i, j, 1] = (result[i, j, 1] + direction * (k ^ 0x33)) % 256
                    result[i, j, 2] = (result[i, j, 2] + direction * (k ^ 0x55)) % 256
                    
        elif method == "swap":
            k = key & 0xFF
            if operation == "encrypt":
                for i in range(h):
                    for j in range(w):
                        r, g, b = result[i, j, 0], result[i, j, 1], result[i, j, 2]
                        result[i, j, 0] = g ^ k
                        result[i, j, 1] = b ^ ((k >> 2) & 0xFF)
                        result[i, j, 2] = r ^ ((k >> 4) & 0xFF)
            else:
                for i in range(h):
                    for j in range(w):
                        r, g, b = result[i, j, 0], result[i, j, 1], result[i, j, 2]
                        r = r ^ k
                        g = g ^ ((k >> 2) & 0xFF)
                        b = b ^ ((k >> 4) & 0xFF)
                        result[i, j, 0] = b
                        result[i, j, 1] = r
                        result[i, j, 2] = g
                        
        elif method == "invert":
            k = key & 0xFF
            if operation == "encrypt":
                for i in range(h):
                    for j in range(w):
                        result[i, j, 0] = (255 - result[i, j, 0]) ^ k
                        result[i, j, 1] = (255 - result[i, j, 1]) ^ (k ^ 0x3C)
                        result[i, j, 2] = (255 - result[i, j, 2]) ^ (k ^ 0xC3)
            else:
                for i in range(h):
                    for j in range(w):
                        result[i, j, 0] = 255 - (result[i, j, 0] ^ k)
                        result[i, j, 1] = 255 - (result[i, j, 1] ^ (k ^ 0x3C))
                        result[i, j, 2] = 255 - (result[i, j, 2] ^ (k ^ 0xC3))
                        
        elif method == "shuffle":
            # Seeded random for deterministic shuffling
            def seeded_rand(seed):
                s = seed
                def next_rand():
                    nonlocal s
                    s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
                    return s / 0xFFFFFFFF
                return next_rand
            
            indices = list(range(h))
            rng = seeded_rand(key)
            for i in range(h - 1, 0, -1):
                j = int(rng() * (i + 1))
                indices[i], indices[j] = indices[j], indices[i]
            
            temp = np.zeros_like(result)
            if operation == "encrypt":
                for src_row, dst_row in enumerate(indices):
                    temp[dst_row] = result[src_row]
            else:
                inv = [0] * h
                for i, idx in enumerate(indices):
                    inv[idx] = i
                for src_row, dst_row in enumerate(inv):
                    temp[dst_row] = result[src_row]
            result = temp
            
        elif method == "multi":
            k = key & 0xFF
            shift = key % 256
            if operation == "encrypt":
                for i in range(h):
                    for j in range(w):
                        result[i, j, 0] = ((result[i, j, 0] + shift) % 256) ^ k
                        result[i, j, 1] = ((result[i, j, 1] + (shift ^ 0x33)) % 256) ^ (k ^ 0x5A)
                        result[i, j, 2] = ((result[i, j, 2] + (shift ^ 0x55)) % 256) ^ (k ^ 0xA5)
            else:
                for i in range(h):
                    for j in range(w):
                        result[i, j, 0] = ((result[i, j, 0] ^ k) - shift + 256) % 256
                        result[i, j, 1] = ((result[i, j, 1] ^ (k ^ 0x5A)) - (shift ^ 0x33) + 256) % 256
                        result[i, j, 2] = ((result[i, j, 2] ^ (k ^ 0xA5)) - (shift ^ 0x55) + 256) % 256
                        
        return result
        
    def update_progress(self, value, text):
        """Update progress bar from background thread"""
        self.window.after(0, lambda: self.progress_bar.set(value))
        self.window.after(0, lambda: self.progress_label.configure(text=text))
        
    def update_after_processing(self, operation, key, method):
        """Update UI after processing"""
        self.progress_frame.pack_forget()
        self.download_btn.pack(pady=10, padx=20, fill="x")
        
        op_text = "Encrypted" if operation == "encrypt" else "Decrypted"
        if self.status_label:
            self.status_label.configure(
                text=f"✅ {op_text} successfully using {method.upper()} with key: {key}"
            )
        
        # Show info
        if self.info_label:
            self.info_label.configure(
                text=f"🔑 Key: {key} | 📐 {self.processed_image.size[0]}×{self.processed_image.size[1]}"
            )
        
    def download_result(self):
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to download!")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=[
                ("PNG image", "*.png"),
                ("JPEG image", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved successfully!\n📍 {file_path}")
                if self.status_label:
                    self.status_label.configure(text=f"✅ Image saved: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                
    def run(self):
        self.window.mainloop()

# ============== Main Entry Point ==============

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔐 PIXEL ENCRYPTION TOOL")
    print("👨‍💻 Developed by: Nitish Sharma")
    print("="*60 + "\n")
    
    app = ImageEncryptionApp()
    app.run()