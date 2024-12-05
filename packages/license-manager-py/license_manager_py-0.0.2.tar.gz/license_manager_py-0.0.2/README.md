# License Manager

## 功能特点

- 生成加密许可证
- 验证许可证有效性
- 支持多设备许可
- 基于时间的许可证到期
- 可自定义许可证特性

## 安装

```bash
pip install license-manager-py
```

## 基本使用

```python
from license_manager import LicenseManager

# 初始化许可证管理器
lm = LicenseManager()

# 生成许可证
license = lm.generate_license(
    customer_name="张三", 
    product_name="数据分析软件",
    valid_days=365,
    max_devices=3
)

# 验证许可证
is_valid = lm.validate_license(license['license_id'], device_id='device001')
```

## 许可证管理

- 生成许可证
- 验证许可证
- 撤销许可证

## 贡献

欢迎提交PR和Issues！

## 许可证

MIT许可证