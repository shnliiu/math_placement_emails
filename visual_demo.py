import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import time
import threading
from ai_agent import MathPlacementAgent

class VisualDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Math Placement Agent - Outlook Style Demo")
        self.root.geometry("1400x900")
        self.root.configure(bg='#ffffff')
        
        self.agent = MathPlacementAgent()
        self.emails = []
        self.current_email_index = 0
        
        self.setup_ui()
        self.load_emails()
        
    def setup_ui(self):
        # Modern gradient toolbar
        toolbar = tk.Frame(self.root, bg='#2c3e50', height=70)
        toolbar.pack(fill=tk.X)
        toolbar.pack_propagate(False)
        
        title = tk.Label(toolbar, text="🤖 AI Math Placement Agent", 
                        font=("SF Pro Display", 18, "bold"), bg='#2c3e50', fg='#ecf0f1')
        title.pack(side=tk.LEFT, padx=25, pady=20)
        
        button_frame = tk.Frame(toolbar, bg='#2c3e50')
        button_frame.pack(side=tk.RIGHT, padx=25, pady=15)
        
        self.start_button = tk.Button(button_frame, text="▶ Start Processing", 
                                     command=self.start_demo, font=("SF Pro Display", 11, "bold"),
                                     bg='#3498db', fg='white', padx=20, pady=10, relief='flat',
                                     cursor='hand2', activebackground='#2980b9')
        self.start_button.pack(side=tk.RIGHT, padx=5)
        
        self.reset_button = tk.Button(button_frame, text="🔄 Reset", 
                                     command=self.reset_demo, font=("SF Pro Display", 11),
                                     bg='#95a5a6', fg='white', padx=20, pady=10, relief='flat',
                                     cursor='hand2', activebackground='#7f8c8d')
        self.reset_button.pack(side=tk.RIGHT, padx=5)
        
        # Main container with modern styling
        main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg='#ecf0f1', 
                                       sashwidth=3, sashrelief='flat')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Modern inbox
        left_panel = tk.Frame(main_container, bg='#ffffff', width=420)
        main_container.add(left_panel, minsize=380)
        
        inbox_header = tk.Frame(left_panel, bg='#34495e', height=50)
        inbox_header.pack(fill=tk.X)
        inbox_header.pack_propagate(False)
        
        tk.Label(inbox_header, text="📧 Inbox", font=("SF Pro Display", 14, "bold"), 
                bg='#34495e', fg='#ecf0f1').pack(side=tk.LEFT, padx=20, pady=15)
        
        self.stats_label = tk.Label(inbox_header, text="Ready", 
                                   font=("SF Pro Display", 10), bg='#34495e', fg='#bdc3c7')
        self.stats_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Modern email list
        list_frame = tk.Frame(left_panel, bg='#ffffff')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.inbox_tree = ttk.Treeview(list_frame, columns=("from", "subject", "status"), 
                                      show="headings", height=18)
        self.inbox_tree.heading("from", text="From")
        self.inbox_tree.heading("subject", text="Subject")
        self.inbox_tree.heading("status", text="Status")
        self.inbox_tree.column("from", width=130)
        self.inbox_tree.column("subject", width=220)
        self.inbox_tree.column("status", width=90)
        
        # Modern treeview styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", font=("SF Pro Display", 10), rowheight=30, 
                       background='#ffffff', foreground='#2c3e50')
        style.configure("Treeview.Heading", font=("SF Pro Display", 10, "bold"),
                       background='#ecf0f1', foreground='#2c3e50')
        style.map('Treeview', background=[('selected', '#3498db')])
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.inbox_tree.yview)
        self.inbox_tree.configure(yscrollcommand=scrollbar.set)
        
        self.inbox_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Modern email view
        right_panel = tk.PanedWindow(main_container, orient=tk.VERTICAL, bg='#ecf0f1',
                                    sashwidth=3, sashrelief='flat')
        main_container.add(right_panel, minsize=700)
        
        # Current email view
        email_frame = tk.Frame(right_panel, bg='#ffffff')
        right_panel.add(email_frame, minsize=220)
        
        email_header = tk.Frame(email_frame, bg='#34495e', height=50)
        email_header.pack(fill=tk.X)
        email_header.pack_propagate(False)
        
        tk.Label(email_header, text="📨 Current Email", font=("SF Pro Display", 14, "bold"), 
                bg='#34495e', fg='#ecf0f1').pack(side=tk.LEFT, padx=20, pady=15)
        
        self.current_email_text = scrolledtext.ScrolledText(email_frame, font=("SF Pro Display", 11),
                                                           bg='#ffffff', fg='#2c3e50', 
                                                           wrap=tk.WORD, padx=20, pady=15,
                                                           relief='flat', borderwidth=0)
        self.current_email_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # AI Response generation
        response_frame = tk.Frame(right_panel, bg='#ffffff')
        right_panel.add(response_frame, minsize=350)
        
        response_header = tk.Frame(response_frame, bg='#27ae60', height=50)
        response_header.pack(fill=tk.X)
        response_header.pack_propagate(False)
        
        tk.Label(response_header, text="🤖 AI Generated Response", font=("SF Pro Display", 14, "bold"), 
                bg='#27ae60', fg='#ffffff').pack(side=tk.LEFT, padx=20, pady=15)
        
        self.ai_status = tk.Label(response_header, text="Waiting...", 
                                 font=("SF Pro Display", 10), bg='#27ae60', fg='#d5f4e6')
        self.ai_status.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.response_text = scrolledtext.ScrolledText(response_frame, font=("SF Pro Display", 11),
                                                      bg='#f8f9fa', fg='#2c3e50', 
                                                      wrap=tk.WORD, padx=20, pady=15,
                                                      relief='flat', borderwidth=0)
        self.response_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
    def load_emails(self):
        try:
            with open('mock_emails.json', 'r') as f:
                self.emails = json.load(f)
            
            # Populate inbox
            for email in self.emails:
                self.inbox_tree.insert("", "end", values=(
                    email['from'], 
                    email['subject'], 
                    "Pending"
                ))
        except FileNotFoundError:
            self.stats_label.config(text="❌ mock_emails.json not found!")
    
    def start_demo(self):
        self.start_button.config(state='disabled')
        self.reset_button.config(state='disabled')
        threading.Thread(target=self.process_emails_visual, daemon=True).start()
    
    def process_emails_visual(self):
        math_placement_count = 0
        
        for i, email in enumerate(self.emails):
            self.current_email_index = i
            
            # Update current email display
            self.root.after(0, self.update_current_email, email)
            self.root.after(0, self.clear_response)
            
            # Step 1: Classification
            self.root.after(0, self.update_ai_status, "Analyzing email...")
            time.sleep(1)
            
            is_math_placement = self.agent.is_math_placement_email(email)
            
            if is_math_placement:
                math_placement_count += 1
                self.root.after(0, self.update_inbox_status, i, "Math Placement ✅")
                self.root.after(0, self.update_ai_status, "Math placement detected! Querying knowledge base...")
                
                # Step 2: Knowledge Base Query
                time.sleep(1.5)
                response_content = self.agent.generate_response(email['body'])
                
                # Step 3: Response Generation with typing effect
                self.root.after(0, self.update_ai_status, "Generating response...")
                time.sleep(0.5)
                
                email_response = self.agent.compose_email_response(email, response_content)
                self.root.after(0, self.type_response, email_response['body'])
                
                # Wait for typing to complete (calculate based on text length)
                typing_time = max(4, len(email_response['body']) * 0.02)
                time.sleep(typing_time)
                
                # Step 4: Email Sending
                self.root.after(0, self.update_ai_status, "Sending response...")
                time.sleep(1)
                
                self.root.after(0, self.update_inbox_status, i, "Response Sent ✅")
                self.root.after(0, self.update_ai_status, "Response sent successfully!")
                
            else:
                self.root.after(0, self.update_inbox_status, i, "Skipped ❌")
                self.root.after(0, self.update_ai_status, "Not a math placement inquiry - skipped")
                self.root.after(0, self.show_skip_message)
            
            # Update stats
            processed = i + 1
            stats_text = f"Processed: {processed}/{len(self.emails)} | Math Placement: {math_placement_count}"
            self.root.after(0, self.update_stats, stats_text)
            
            time.sleep(2)
        
        # Final completion
        final_stats = f"✅ Complete! {len(self.emails)} processed | {math_placement_count} responses sent"
        self.root.after(0, self.update_stats, final_stats)
        self.root.after(0, self.update_ai_status, "Processing complete!")
        self.root.after(0, lambda: self.reset_button.config(state='normal'))
    
    def update_current_email(self, email):
        self.current_email_text.delete(1.0, tk.END)
        content = f"From: {email['from']}\nSubject: {email['subject']}\nReceived: Just now\n\n{email['body']}"
        self.current_email_text.insert(1.0, content)
    
    def update_inbox_status(self, row_index, status):
        item = self.inbox_tree.get_children()[row_index]
        values = list(self.inbox_tree.item(item, 'values'))
        values[2] = status
        self.inbox_tree.item(item, values=values)
    
    def update_stats(self, text):
        self.stats_label.config(text=text)
    
    def update_ai_status(self, text):
        self.ai_status.config(text=text)
    
    def clear_response(self):
        self.response_text.delete(1.0, tk.END)
    
    def type_response(self, response_text):
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(1.0, "Generating response...\n\n")
        self.response_text.config(fg='#7f8c8d')
        self.root.after(1000, self._start_typing, response_text)
    
    def _start_typing(self, response_text):
        self.response_text.delete(1.0, tk.END)
        self.response_text.config(fg='#2c3e50')
        self._typing_response(response_text, 0)
    
    def _typing_response(self, text, index):
        if index < len(text):
            self.response_text.insert(tk.END, text[index])
            self.response_text.see(tk.END)
            self.root.after(15, self._typing_response, text, index + 1)
        else:
            # Show completion effect
            self.root.after(500, self._show_completion_effect)
    
    def _show_completion_effect(self):
        self.ai_status.config(text="Response generated! ✨", fg='#ffffff')
        # Brief highlight effect
        original_bg = self.response_text.cget('bg')
        self.response_text.config(bg='#e8f5e8')
        self.root.after(1000, lambda: self.response_text.config(bg=original_bg))
    
    def show_skip_message(self):
        skip_msg = "This email does not appear to be related to math placement and will be skipped."
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(1.0, skip_msg)
    
    def reset_demo(self):
        # Reset inbox
        for item in self.inbox_tree.get_children():
            values = list(self.inbox_tree.item(item, 'values'))
            values[2] = "Pending"
            self.inbox_tree.item(item, values=values)
        
        # Reset displays
        self.current_email_text.delete(1.0, tk.END)
        self.response_text.delete(1.0, tk.END)
        
        # Reset status and buttons
        self.stats_label.config(text="Ready")
        self.ai_status.config(text="Waiting...")
        self.start_button.config(state='normal')
        self.reset_button.config(state='normal')
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    demo = VisualDemo()
    demo.run()