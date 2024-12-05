import os
import json
import uuid
from datetime import datetime, timedelta
import hashlib
import base64
from cryptography.fernet import Fernet


class LicenseManager:
    def __init__(self, storage_path='licenses.json', encryption_key=None):
        """
        初始化许可证管理器

        :param storage_path: 许可证存储文件路径
        :param encryption_key: 加密密钥，为None时自动生成
        """
        self.storage_path = storage_path

        # 如果没有提供加密密钥，则生成
        if encryption_key is None:
            encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(encryption_key)

        # 确保存储文件存在
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump({}, f)

    def generate_license(self,
                         customer_name,
                         product_name,
                         valid_days=365,
                         max_devices=1,
                         features=None):
        """
        生成许可证

        :param customer_name: 客户名称
        :param product_name: 产品名称
        :param valid_days: 有效天数
        :param max_devices: 最大设备数
        :param features: 许可证特性
        :return: 许可证信息
        """
        license_id = str(uuid.uuid4())
        current_time = datetime.now()
        expiry_time = current_time + timedelta(days=valid_days)

        license_data = {
            'license_id': license_id,
            'customer_name': customer_name,
            'product_name': product_name,
            'created_at': current_time.isoformat(),
            'expires_at': expiry_time.isoformat(),
            'max_devices': max_devices,
            'current_devices': 0,
            'features': features or [],
            'status': 'active'
        }

        # 加密许可证数据
        encrypted_license = self._encrypt_license(license_data)

        # 存储许可证
        licenses = self._load_licenses()
        licenses[license_id] = encrypted_license
        self._save_licenses(licenses)

        return license_data

    def validate_license(self, license_id, device_id=None):
        """
        验证许可证有效性

        :param license_id: 许可证ID
        :param device_id: 设备ID
        :return: 是否有效
        """
        licenses = self._load_licenses()
        if license_id not in licenses:
            return False

        # 解密许可证
        license_data = self._decrypt_license(licenses[license_id])

        # 检查过期时间
        expiry_time = datetime.fromisoformat(license_data['expires_at'])
        if datetime.now() > expiry_time:
            license_data['status'] = 'expired'
            licenses[license_id] = self._encrypt_license(license_data)
            self._save_licenses(licenses)
            return False

        # 检查设备数量限制
        if device_id:
            if license_data['current_devices'] >= license_data['max_devices']:
                return False
            license_data['current_devices'] += 1

        # 更新许可证
        licenses[license_id] = self._encrypt_license(license_data)
        self._save_licenses(licenses)

        return True

    def revoke_license(self, license_id):
        """
        撤销许可证

        :param license_id: 许可证ID
        """
        licenses = self._load_licenses()
        if license_id in licenses:
            license_data = self._decrypt_license(licenses[license_id])
            license_data['status'] = 'revoked'
            licenses[license_id] = self._encrypt_license(license_data)
            self._save_licenses(licenses)

    def _encrypt_license(self, license_data):
        """
        加密许可证数据

        :param license_data: 许可证数据
        :return: 加密后的许可证
        """
        serialized_data = json.dumps(license_data).encode()
        encrypted_data = self.cipher_suite.encrypt(serialized_data)
        return base64.b64encode(encrypted_data).decode()

    def _decrypt_license(self, encrypted_license):
        """
        解密许可证数据

        :param encrypted_license: 加密的许可证
        :return: 解密后的许可证数据
        """
        decrypted_data = self.cipher_suite.decrypt(
            base64.b64decode(encrypted_license.encode())
        )
        return json.loads(decrypted_data.decode())

    def _load_licenses(self):
        """
        加载所有许可证
        """
        with open(self.storage_path, 'r') as f:
            return json.load(f)

    def _save_licenses(self, licenses):
        """
        保存所有许可证
        """
        with open(self.storage_path, 'w') as f:
            json.dump(licenses, f, indent=2)