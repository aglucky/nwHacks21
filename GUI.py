import dearpygui.core as dpg
import dearpygui.simple as sdpg
import stock_market_predictions


class stockApp:
    def __init__(self, stocks):
        self.stocks = stocks

    def __render(self, sender, data):
        """Run every frame to update the GUI.
        Updates the table by clearing it and inserting rows with the data.
        """
        dpg.clear_table("Stocks")
        for stock in self.stocks:
            dpg.add_row("Stocks", [stock["Prediction"], stock["Confidence"]])

    def __add_stock(self, sender, data):
        """Add a new todo.
        Get the data from the input text, append a new todo to the todos list
        and then clear the text of the input.
        """
        new_tickr = dpg.get_value("stock-ticker")
        stock_pred, confidence = stock_market_predictions.stockPredict("AAPL")
        new_entry = {
            "Stock": new_tickr,
            "Prediction": stock_pred,
            "Confidence": confidence,
        }
        self.stocks.append(new_entry)
        dpg.set_value("stock-ticker", "")

    def __remove_stock(self, sender, data):
        """Remove a todo from the todos list based on the selected row."""
        stock_index = dpg.get_data("selected-stock-index")
        self.stocks.pop(stock_index)

    def __clear_stocks(self, sender, data):
        """Clear all the todos."""
        self.stocks = []

    def show(self):
        """Start the gui."""
        with sdpg.window("Main Window"):
            dpg.set_main_window_size(550, 550)
            dpg.set_main_window_resizable(False)
            dpg.set_main_window_title("Stock Prediction App")

            dpg.add_text("Stock App")
            dpg.add_text(
                "Add a stock by writing a title and clicking",
                " the add stock button",
                bullet=True,
            )
            dpg.add_text("Toggle a stock by clicking on its table row", bullet=True)
            dpg.add_text(
                "Remove a stock by clicking on its table row and clicking"
                " the remove stock button",
                bullet=True,
            )
            dpg.add_separator()

            dpg.add_spacing(count=10)
            dpg.add_input_text("Stock Ticker", source="stock-ticker")
            dpg.add_button("Add Stock", callback=self.__add_stock)
            dpg.add_spacing(count=10)
            dpg.add_separator()

            dpg.add_table(
                "Stocks",
                ["Stock", "Prediction", "Confidence"],
                height=200,
            )
            dpg.add_separator()
            dpg.add_text("Selected stock:")
            dpg.add_button("Remove stock", callback=self.__remove_stock)
            dpg.add_button("Clear stocks", callback=self.__clear_stocks)

            # Render Callback and Start gui
            dpg.set_render_callback(self.__render)
        dpg.start_dearpygui(primary_window="Main Window")


if __name__ == "__main__":
    amzn = "AMZN"
    stocks = []

    stock_app = stockApp(stocks)
    stock_app.show()
