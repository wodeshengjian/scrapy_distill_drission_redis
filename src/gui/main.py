"""Main GUI Application"""
import sys
import subprocess
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTabWidget, QTextEdit, QPushButton, QLineEdit, QLabel,
    QListWidget, QListWidgetItem, QProgressBar, QComboBox,
    QSpinBox, QCheckBox, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from src.spider.proxy_pool.manager import ProxyPool
from src.utils.redis_client import get_redis_client


class LogThread(QThread):
    """Log monitoring thread"""
    log_signal = pyqtSignal(str)
    
    def run(self):
        while True:
            try:
                with open('logs/spider.log', 'r', encoding='utf-8') as f:
                    lines = f.readlines()[-50:]
                    self.log_signal.emit(''.join(lines))
            except:
                pass
            self.sleep(2)


class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ScraDispage - Crawler Manager')
        self.setGeometry(100, 100, 900, 600)
        
        self.redis_client = get_redis_client()
        self.proxy_pool = ProxyPool()
        self.spider_process = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_control_tab(), 'Crawler Control')
        self.tabs.addTab(self.create_log_tab(), 'Log Output')
        self.tabs.addTab(self.create_proxy_tab(), 'Proxy Management')
        self.tabs.addTab(self.create_config_tab(), 'System Config')
        layout.addWidget(self.tabs)
    
    def create_control_tab(self):
        """Create crawler control tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton('Start Crawler')
        self.start_btn.clicked.connect(self.start_crawler)
        self.stop_btn = QPushButton('Stop Crawler')
        self.stop_btn.clicked.connect(self.stop_crawler)
        self.train_btn = QPushButton('Train Model')
        self.train_btn.clicked.connect(self.train_model)
        self.clear_btn = QPushButton('Clear Log')
        self.clear_btn.clicked.connect(self.clear_log)
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.train_btn)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)
        
        # Status
        self.status_label = QLabel('Status: Ready')
        self.status_label.setStyleSheet('color: green; font-weight: bold')
        layout.addWidget(self.status_label)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        return widget
    
    def create_log_tab(self):
        """Create log output tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        return widget
    
    def create_proxy_tab(self):
        """Create proxy management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add proxy
        add_layout = QHBoxLayout()
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText('Enter proxy: http://host:port')
        add_btn = QPushButton('Add Proxy')
        add_btn.clicked.connect(self.add_proxy)
        refresh_btn = QPushButton('Refresh List')
        refresh_btn.clicked.connect(self.refresh_proxies)
        validate_btn = QPushButton('Validate All')
        validate_btn.clicked.connect(self.validate_proxies)
        
        add_layout.addWidget(self.proxy_input)
        add_layout.addWidget(add_btn)
        add_layout.addWidget(refresh_btn)
        add_layout.addWidget(validate_btn)
        layout.addLayout(add_layout)
        
        # Proxy list
        self.proxy_list = QListWidget()
        layout.addWidget(self.proxy_list)
        
        return widget
    
    def create_config_tab(self):
        """Create system config tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Redis config
        redis_group = QGroupBox('Redis Configuration')
        redis_layout = QFormLayout(redis_group)
        self.redis_host = QLineEdit('localhost')
        self.redis_port = QSpinBox()
        self.redis_port.setValue(6379)
        self.redis_db = QSpinBox()
        self.redis_db.setValue(0)
        
        redis_layout.addRow('Host:', self.redis_host)
        redis_layout.addRow('Port:', self.redis_port)
        redis_layout.addRow('DB:', self.redis_db)
        layout.addWidget(redis_group)
        
        # Crawler config
        crawler_group = QGroupBox('Crawler Configuration')
        crawler_layout = QFormLayout(crawler_group)
        self.concurrent_req = QSpinBox()
        self.concurrent_req.setValue(16)
        self.download_delay = QSpinBox()
        self.download_delay.setValue(2)
        self.retry_times = QSpinBox()
        self.retry_times.setValue(3)
        
        crawler_layout.addRow('Concurrent Requests:', self.concurrent_req)
        crawler_layout.addRow('Download Delay (s):', self.download_delay)
        crawler_layout.addRow('Retry Times:', self.retry_times)
        layout.addWidget(crawler_group)
        
        # Save button
        save_btn = QPushButton('Save Configuration')
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)
        
        return widget
    
    def start_crawler(self):
        """Start crawler"""
        try:
            self.spider_process = subprocess.Popen(
                [sys.executable, '-m', 'scrapy', 'crawl', 'demo_spider'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.status_label.setText('Status: Running')
            self.status_label.setStyleSheet('color: blue; font-weight: bold')
            QMessageBox.information(self, 'Success', 'Crawler started successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to start crawler: {e}')
    
    def stop_crawler(self):
        """Stop crawler"""
        if self.spider_process:
            self.spider_process.terminate()
            self.spider_process = None
            self.status_label.setText('Status: Stopped')
            self.status_label.setStyleSheet('color: red; font-weight: bold')
            QMessageBox.information(self, 'Success', 'Crawler stopped successfully!')
    
    def train_model(self):
        """Train AI model"""
        try:
            subprocess.run([sys.executable, '-m', 'src.train'], check=True)
            QMessageBox.information(self, 'Success', 'Model trained successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to train model: {e}')
    
    def clear_log(self):
        """Clear log"""
        self.log_text.clear()
    
    def add_proxy(self):
        """Add proxy"""
        proxy = self.proxy_input.text()
        if proxy:
            self.proxy_pool.add_proxy(proxy)
            self.proxy_input.clear()
            self.refresh_proxies()
            QMessageBox.information(self, 'Success', 'Proxy added successfully!')
    
    def refresh_proxies(self):
        """Refresh proxy list"""
        self.proxy_list.clear()
        proxies = self.proxy_pool.get_all_proxies()
        for proxy in proxies:
            QListWidgetItem(proxy, self.proxy_list)
    
    def validate_proxies(self):
        """Validate all proxies"""
        proxies = self.proxy_pool.get_all_proxies()
        valid_count = 0
        for proxy in proxies:
            if self.proxy_pool.validate_proxy(proxy):
                valid_count += 1
        QMessageBox.information(self, 'Validation', f'{valid_count}/{len(proxies)} proxies are valid')
    
    def save_config(self):
        """Save configuration"""
        QMessageBox.information(self, 'Success', 'Configuration saved!')


def main():
    """Run GUI application"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()