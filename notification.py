import price
import os

def check_price_notification(buy_price, sell_price):
    """
    检查当前价格是否低于买入价或高于卖出价，并返回相应的通知消息。
    
    :param buy_price: 设置的买入价
    :param sell_price: 设置的卖出价
    :return: 通知消息（如果价格符合条件）
    """
    current_price = price.get_current_price()
    if current_price < buy_price:
        return f"当前价格 {current_price} 低于设置的买入价 {buy_price}，建议买入。"
    elif current_price > sell_price:
        return f"当前价格 {current_price} 高于设置的卖出价 {sell_price}，建议卖出。"
    else:
        return None


def send_notification(message):
    """
    发送通知消息（调用 sendNotice 模块的 bark 方法推送消息）。
    
    :param message: 通知消息
    """
    if message:
        from sendNotice import bark
        bark("金价提醒", message)


if __name__ == "__main__":
    # 示例用法

    buy_price = float(os.getenv("gold_buy_price")) if os.getenv("gold_buy_price") else 900
    sell_price = float(os.getenv("gold_sell_price")) if os.getenv("gold_sell_price") else 950
    
    notification = check_price_notification(buy_price, sell_price)
    print(notification)
    send_notification(notification)