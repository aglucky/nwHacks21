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
            dpg.add_row(
                "Stocks", [stock["Stock"], stock["Prediction"], stock["Confidence"]]
            )

    def __toggle_stock(self, sender, data):
        """Toggle a todo to True of False.
        Get the selected cell of the table (list of [row index, column index])
        and uses the row index to update the todo at that index in the todos
        list. Then, saves the selected row index in the case you would want to
        delete that todo.
        """
        stock_row = dpg.get_table_selections("Stocks")
        stock = self.stocks[stock_row[0][0]]
        dpg.add_data("selected-stock-index", self.stocks.index(stock))
        dpg.set_value("Selected stock:", f"Selected Stock: {stock['Stock']}")

    def __add_stock(self, sender, data):
        """Add a new todo.
        Get the data from the input text, append a new todo to the todos list
        and then clear the text of the input.
        """
        new_tickr = dpg.get_value("stock-ticker")
        stock_pred, confidence = stock_market_predictions.stockPredict(new_tickr)
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
            dpg.set_main_window_size(550, 600)
            dpg.set_main_window_resizable(False)
            dpg.set_main_window_title("Stockify")

            dpg.add_text("Stockify: The Future of Stocks")
            dpg.add_text(
                "Predict a stock by typing in its ticker and clicking"
                " the predict stock button",
                bullet=True,
            )
            dpg.add_text(
                "Remove a stock by clicking on its table row and clicking"
                " the remove stock button",
                bullet=True,
            )
            dpg.add_text(
                "All predictions will predict a stocks value " "in 30 days",
                bullet=True,
            )

            dpg.add_text(
                "Confidence is the degree that Stockify"
                " is sure about its prediction",
                bullet=True,
            )
            dpg.add_separator()

            dpg.add_spacing(count=10)
            dpg.add_input_text("Stock Ticker", source="stock-ticker")
            dpg.add_button("Predict Stock", callback=self.__add_stock)
            dpg.add_spacing(count=10)
            dpg.add_separator()

            dpg.add_table(
                "Stocks",
                ["Stock", "Prediction", "Confidence"],
                height=200,
                callback=self.__toggle_stock,
            )
            dpg.add_separator()
            dpg.add_text("Selected stock:")
            dpg.add_button("Remove stock", callback=self.__remove_stock)
            dpg.add_button("Clear stocks", callback=self.__clear_stocks)

            # Render Callback and Start gui
            dpg.set_render_callback(self.__render)
        dpg.start_dearpygui(primary_window="Main Window")


if __name__ == "__main__":
    stocks = []

    stock_app = stockApp(stocks)
    stock_app.show()
