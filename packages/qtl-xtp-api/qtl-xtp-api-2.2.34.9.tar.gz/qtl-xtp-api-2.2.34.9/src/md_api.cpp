#include "md_api.h"


void MdApi::CreateQuoteApi(int client_id, const std::string &save_file_path, int log_level) {
    queue_ = std::make_unique<DispatchQueue>();
    api_ = xtp::QuoteApi::CreateQuoteApi(client_id, save_file_path.c_str(), XTP_LOG_LEVEL(log_level));
    api_->RegisterSpi(this);
}

void MdApi::Destroy() {
    api_->RegisterSpi(nullptr);
    api_->Release();
    api_ = nullptr;
    queue_ = nullptr;
}

std::string MdApi::GetTradingDay() {
    return api_->GetTradingDay();
}

std::string MdApi::GetApiVersion() {
    return api_->GetApiVersion();
}

nb::dict MdApi::GetApiLastError() {
    auto *error_ = api_->GetApiLastError();
    nb::dict error{};
    error["error_id"] = error_->error_id;
    error["error_msg"] = error_->error_msg;
    return error;
}

void MdApi::SetUDPBufferSize(uint32_t buff_size) {
    api_->SetUDPBufferSize(buff_size);
}

void MdApi::SetHeartBeatInterval(uint32_t interval) {
    api_->SetHeartBeatInterval(interval);
}

void MdApi::SetUDPRecvThreadAffinity(int32_t cpu_no) {
    api_->SetUDPRecvThreadAffinity(cpu_no);
}

void MdApi::SetUDPRecvThreadAffinityArray(const std::vector<int32_t> &cpu_no_array) {
    api_->SetUDPRecvThreadAffinityArray(
            const_cast<int32_t *>(cpu_no_array.data()),
            cpu_no_array.size()
    );
}

void MdApi::SetUDPParseThreadAffinity(int32_t cpu_no) {
    api_->SetUDPParseThreadAffinity(cpu_no);
}

void MdApi::SetUDPParseThreadAffinityArray(const std::vector<int32_t> &cpu_no_array) {
    api_->SetUDPParseThreadAffinityArray(
        const_cast<int32_t *>(cpu_no_array.data()),
        cpu_no_array.size()
    );
}

void MdApi::SetUDPSeqLogOutPutFlag(bool flag) {
    api_->SetUDPSeqLogOutPutFlag(flag);
}

int MdApi::SubscribeMarketData(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id) {
    std::vector<char *> ticker_{};
    for (const auto &i : ticker) {
        ticker_.emplace_back(const_cast<char *>(i.c_str()));
    }
    return api_->SubscribeMarketData(ticker_.data(), ticker_.size(), exchange_id);
}

int MdApi::UnSubscribeMarketData(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id) {
    std::vector<char *> ticker_{};
    for (const auto &i : ticker) {
        ticker_.emplace_back(const_cast<char *>(i.c_str()));
    }
    return api_->UnSubscribeMarketData(ticker_.data(), ticker_.size(), exchange_id);
}

int MdApi::SubscribeOrderBook(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id) {
    std::vector<char *> ticker_{};
    for (const auto &i : ticker) {
        ticker_.emplace_back(const_cast<char *>(i.c_str()));
    }
    return api_->SubscribeOrderBook(ticker_.data(), ticker_.size(), exchange_id);
}

int MdApi::UnSubscribeOrderBook(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id) {
    std::vector<char *> ticker_{};
    for (const auto &i : ticker) {
        ticker_.emplace_back(const_cast<char *>(i.c_str()));
    }
    return api_->UnSubscribeOrderBook(ticker_.data(), ticker_.size(), exchange_id);
}

int MdApi::SubscribeTickByTick(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id) {
    std::vector<char *> ticker_{};
    for (const auto &i : ticker) {
        ticker_.emplace_back(const_cast<char *>(i.c_str()));
    }
    return api_->SubscribeTickByTick(ticker_.data(), ticker_.size(), exchange_id);
}

int MdApi::UnSubscribeTickByTick(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id) {
    std::vector<char *> ticker_{};
    for (const auto &i : ticker) {
        ticker_.emplace_back(const_cast<char *>(i.c_str()));
    }
    return api_->UnSubscribeTickByTick(ticker_.data(), ticker_.size(), exchange_id);
}

int MdApi::SubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->SubscribeAllMarketData(exchange_id);
}

int MdApi::UnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->UnSubscribeAllMarketData(exchange_id);
}

int MdApi::SubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->SubscribeAllOrderBook(exchange_id);
}

int MdApi::UnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->UnSubscribeAllOrderBook(exchange_id);
}

int MdApi::SubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->SubscribeAllTickByTick(exchange_id);
}

int MdApi::UnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->UnSubscribeAllTickByTick(exchange_id);
}

int MdApi::Login(const char *ip, int port, const char *user, const char *password, XTP_PROTOCOL_TYPE sock_type,
                 const char *local_ip) {
    return api_->Login(ip, port, user, password, sock_type, local_ip);
}

int MdApi::Logout() {
    return api_->Logout();
}

int MdApi::QueryAllTickers(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->QueryAllTickers(exchange_id);
}

int MdApi::QueryTickersPriceInfo(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id) {
    std::vector<char *> ticker_{};
    for (const auto &i : ticker) {
        ticker_.emplace_back(const_cast<char *>(i.c_str()));
    }
    return api_->QueryTickersPriceInfo(ticker_.data(), ticker_.size(), exchange_id);
}

int MdApi::QueryAllTickersPriceInfo() {
    return api_->QueryAllTickersPriceInfo();
}

int MdApi::SubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->SubscribeAllOptionMarketData(exchange_id);
}

int MdApi::UnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->UnSubscribeAllOptionMarketData(exchange_id);
}

int MdApi::SubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->SubscribeAllOptionOrderBook(exchange_id);
}

int MdApi::UnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->UnSubscribeAllOptionOrderBook(exchange_id);
}

int MdApi::SubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->SubscribeAllOptionTickByTick(exchange_id);
}

int MdApi::UnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->UnSubscribeAllOptionTickByTick(exchange_id);
}

int MdApi::QueryAllTickersFullInfo(XTP_EXCHANGE_TYPE exchange_id) {
    return api_->QueryAllTickersFullInfo(exchange_id);
}

int MdApi::QueryAllNQTickersFullInfo() {
    return api_->QueryAllNQTickersFullInfo();
}

int MdApi::LoginToRebuildQuoteServer(const char *ip, int port, const char *user, const char *password,
                                     XTP_PROTOCOL_TYPE sock_type, const char *local_ip) {
    return api_->LoginToRebuildQuoteServer(ip, port, user, password, sock_type, local_ip);
}

int MdApi::LogoutFromRebuildQuoteServer() {
    return api_->LogoutFromRebuildQuoteServer();
}

int MdApi::RequestRebuildQuote(const nb::dict &rebuild_param) {
    XTPQuoteRebuildReq req{};
    set_num_field<int32_t>(req.request_id, rebuild_param, "request_id");
    set_num_field<XTP_QUOTE_REBUILD_DATA_TYPE>(req.data_type, rebuild_param, "data_type");
    set_num_field<XTP_EXCHANGE_TYPE>(req.exchange_id, rebuild_param, "exchange_id");
    set_str_field(req.ticker, rebuild_param, "ticker", sizeof(req.ticker));
    set_num_field<int16_t>(req.channel_number, rebuild_param, "channel_number");
    set_num_field<int64_t>(req.begin, rebuild_param, "begin");
    set_num_field<int64_t>(req.end, rebuild_param, "end");
    return api_->RequestRebuildQuote(&req);
}

void MdApi::OnDisconnected(int reason) {
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        PyOnDisconnected(reason);
    });
}

void MdApi::OnError(XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnError(py_error);
    });
}

void MdApi::OnSubMarketData(XTPST *ticker, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPST ticker_{};
    if (ticker) {
        has_data = true;
        ticker_ = *ticker;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker{};
        if (has_data) {
            py_ticker["exchange_id"] = ticker_.exchange_id;
            py_ticker["ticker"] = ticker_.ticker;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnSubMarketData(py_ticker, py_error, is_last);
    });
}

void MdApi::OnUnSubMarketData(XTPST *ticker, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPST ticker_{};
    if (ticker) {
        has_data = true;
        ticker_ = *ticker;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker{};
        if (has_data) {
            py_ticker["exchange_id"] = ticker_.exchange_id;
            py_ticker["ticker"] = ticker_.ticker;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnUnSubMarketData(py_ticker, py_error, is_last);
    });
}

void MdApi::OnDepthMarketData(XTPMD *market_data, int64_t bid1_qty[], int32_t bid1_count, int32_t max_bid1_count,
                              int64_t ask1_qty[], int32_t ask1_count, int32_t max_ask1_count) {
    bool has_data{false};
    XTPMD market_data_{};
    if (market_data) {
        has_data = true;
        market_data_ = *market_data;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_market_data{};
        if (has_data) {
            py_market_data["exchange_id"] = market_data_.exchange_id;
            py_market_data["ticker"] = market_data_.ticker;
            py_market_data["last_price"] = market_data_.last_price;
            py_market_data["pre_close_price"] = market_data_.pre_close_price;
            py_market_data["open_price"] = market_data_.open_price;
            py_market_data["high_price"] = market_data_.high_price;
            py_market_data["low_price"] = market_data_.low_price;
            py_market_data["close_price"] = market_data_.close_price;
            py_market_data["pre_total_long_positon"] = market_data_.pre_total_long_positon;
            py_market_data["total_long_positon"] = market_data_.total_long_positon;
            py_market_data["pre_settl_price"] = market_data_.pre_settl_price;
            py_market_data["settl_price"] = market_data_.settl_price;
            py_market_data["upper_limit_price"] = market_data_.upper_limit_price;
            py_market_data["lower_limit_price"] = market_data_.lower_limit_price;
            py_market_data["pre_delta"] = market_data_.pre_delta;
            py_market_data["curr_delta"] = market_data_.curr_delta;
            py_market_data["data_time"] = market_data_.data_time;
            py_market_data["qty"] = market_data_.qty;
            py_market_data["turnover"] = market_data_.turnover;
            py_market_data["avg_price"] = market_data_.avg_price;

            nb::list bid_{};
            nb::list ask_{};
            nb::list bid_qty_{};
            nb::list ask_qty_{};
            for (int i = 0; i < 10; i++) {
                bid_.append(market_data_.bid[i]);
                ask_.append(market_data_.ask[i]);
                bid_qty_.append(market_data_.bid_qty[i]);
                ask_qty_.append(market_data_.ask_qty[i]);
            }
            py_market_data["bid"] = bid_;
            py_market_data["ask"] = ask_;
            py_market_data["bid_qty"] = bid_qty_;
            py_market_data["ask_qty"] = ask_qty_;

            py_market_data["trades_count"] = market_data_.trades_count;
            py_market_data["ticker_status"] = market_data_.ticker_status;

            switch (market_data_.data_type_v2) {
                case XTP_MARKETDATA_V2_ACTUAL:
                    py_market_data["total_bid_qty"] = market_data_.stk.total_bid_qty;
                    py_market_data["total_ask_qty"] = market_data_.stk.total_ask_qty;
                    py_market_data["ma_bid_price"] = market_data_.stk.ma_bid_price;
                    py_market_data["ma_ask_price"] = market_data_.stk.ma_ask_price;
                    py_market_data["ma_bond_bid_price"] = market_data_.stk.ma_bond_bid_price;
                    py_market_data["ma_bond_ask_price"] = market_data_.stk.ma_bond_ask_price;
                    py_market_data["yield_to_maturity"] = market_data_.stk.yield_to_maturity;
                    py_market_data["iopv"] = market_data_.stk.iopv;
                    py_market_data["etf_buy_count"] = market_data_.stk.etf_buy_count;
                    py_market_data["etf_sell_count"] = market_data_.stk.etf_sell_count;
                    py_market_data["etf_buy_qty"] = market_data_.stk.etf_buy_qty;
                    py_market_data["etf_buy_money"] = market_data_.stk.etf_buy_money;
                    py_market_data["etf_sell_money"] = market_data_.stk.etf_sell_money;
                    py_market_data["total_warrant_exec_qty"] = market_data_.stk.total_warrant_exec_qty;
                    py_market_data["warrant_lower_price"] = market_data_.stk.warrant_lower_price;
                    py_market_data["warrant_upper_price"] = market_data_.stk.warrant_upper_price;
                    py_market_data["cancel_buy_count"] = market_data_.stk.cancel_buy_count;
                    py_market_data["cancel_sell_count"] = market_data_.stk.cancel_sell_count;
                    py_market_data["cancel_buy_qty"] = market_data_.stk.cancel_buy_qty;
                    py_market_data["cancel_sell_qty"] = market_data_.stk.cancel_sell_qty;
                    py_market_data["cancel_buy_money"] = market_data_.stk.cancel_buy_money;
                    py_market_data["cancel_sell_money"] = market_data_.stk.cancel_sell_money;
                    py_market_data["total_buy_count"] = market_data_.stk.total_buy_count;
                    py_market_data["total_sell_count"] = market_data_.stk.total_sell_count;
                    py_market_data["duration_after_buy"] = market_data_.stk.duration_after_buy;
                    py_market_data["duration_after_sell"] = market_data_.stk.duration_after_sell;
                    py_market_data["num_bid_orders"] = market_data_.stk.num_bid_orders;
                    py_market_data["num_ask_orders"] = market_data_.stk.num_ask_orders;
                    py_market_data["pre_iopv"] = market_data_.stk.pre_iopv;
                    py_market_data["r1"] = market_data_.stk.r1;
                    py_market_data["r2"] = market_data_.stk.r2;
                    break;
                case XTP_MARKETDATA_V2_OPTION:
                    py_market_data["auction_price"] = market_data_.opt.auction_price;
                    py_market_data["auction_qty"] = market_data_.opt.auction_qty;
                    py_market_data["last_enquiry_time"] = market_data_.opt.last_enquiry_time;
                    break;
                case XTP_MARKETDATA_V2_BOND:
                    py_market_data["total_bid_qty"] = market_data_.bond.total_bid_qty;
                    py_market_data["total_ask_qty"] = market_data_.bond.total_ask_qty;
                    py_market_data["ma_bid_price"] = market_data_.bond.ma_bid_price;
                    py_market_data["ma_ask_price"] = market_data_.bond.ma_ask_price;
                    py_market_data["ma_bond_bid_price"] = market_data_.bond.ma_bond_bid_price;
                    py_market_data["ma_bond_ask_price"] = market_data_.bond.ma_bond_ask_price;
                    py_market_data["yield_to_maturity"] = market_data_.bond.yield_to_maturity;
                    py_market_data["match_lastpx"] = market_data_.bond.match_lastpx;
                    py_market_data["ma_bond_price"] = market_data_.bond.ma_bond_price;
                    py_market_data["match_qty"] = market_data_.bond.match_qty;
                    py_market_data["match_turnover"] = market_data_.bond.match_turnover;
                    py_market_data["r4"] = market_data_.bond.r4;
                    py_market_data["r5"] = market_data_.bond.r5;
                    py_market_data["r6"] = market_data_.bond.r6;
                    py_market_data["r7"] = market_data_.bond.r7;
                    py_market_data["r8"] = market_data_.bond.r8;
                    py_market_data["cancel_buy_count"] = market_data_.bond.cancel_buy_count;
                    py_market_data["cancel_sell_count"] = market_data_.bond.cancel_sell_count;
                    py_market_data["cancel_buy_qty"] = market_data_.bond.cancel_buy_qty;
                    py_market_data["cancel_sell_qty"] = market_data_.bond.cancel_sell_qty;
                    py_market_data["cancel_buy_money"] = market_data_.bond.cancel_buy_money;
                    py_market_data["cancel_sell_money"] = market_data_.bond.cancel_sell_money;
                    py_market_data["total_buy_count"] = market_data_.bond.total_buy_count;
                    py_market_data["total_sell_count"] = market_data_.bond.total_sell_count;
                    py_market_data["duration_after_buy"] = market_data_.bond.duration_after_buy;
                    py_market_data["duration_after_sell"] = market_data_.bond.duration_after_sell;
                    py_market_data["num_bid_orders"] = market_data_.bond.num_bid_orders;
                    py_market_data["num_ask_orders"] = market_data_.bond.num_ask_orders;
                    py_market_data["instrument_status"] = market_data_.bond.instrument_status;
                    break;
                default:
                    break;
            }

            py_market_data["data_type"] = market_data_.data_type;
            py_market_data["data_type_v2"] = market_data_.data_type_v2;
        }
        std::vector<int64_t> py_bid1_qty(bid1_qty, bid1_qty + bid1_count);
        std::vector<int64_t> py_ask1_qty(ask1_qty, ask1_qty + ask1_count);
        PyOnDepthMarketData(py_market_data, py_bid1_qty, max_bid1_count, py_ask1_qty, max_ask1_count);
    });
}

void MdApi::OnSubOrderBook(XTPST *ticker, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPST ticker_{};
    if (ticker) {
        has_data = true;
        ticker_ = *ticker;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker{};
        if (has_data) {
            py_ticker["exchange_id"] = ticker_.exchange_id;
            py_ticker["ticker"] = ticker_.ticker;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnSubOrderBook(py_ticker, py_error, is_last);
    });
}

void MdApi::OnUnSubOrderBook(XTPST *ticker, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPST ticker_{};
    if (ticker) {
        has_data = true;
        ticker_ = *ticker;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker{};
        if (has_data) {
            py_ticker["exchange_id"] = ticker_.exchange_id;
            py_ticker["ticker"] = ticker_.ticker;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnUnSubOrderBook(py_ticker, py_error, is_last);
    });
}

void MdApi::OnOrderBook(XTPOB *order_book) {
    bool has_data{false};
    XTPOB order_book_{};
    if (order_book) {
        has_data = true;
        order_book_ = *order_book;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_order_book{};
        if (has_data) {
            py_order_book["exchange_id"] = order_book_.exchange_id;
            py_order_book["ticker"] = order_book_.ticker;
            py_order_book["last_price"] = order_book_.last_price;
            py_order_book["qty"] = order_book_.qty;
            py_order_book["turnover"] = order_book_.turnover;
            py_order_book["trades_count"] = order_book_.trades_count;
            nb::list bid_{};
            nb::list ask_{};
            nb::list bid_qty_{};
            nb::list ask_qty_{};
            for (int i = 0; i < 10; i++) {
                bid_.append(order_book_.bid[i]);
                ask_.append(order_book_.ask[i]);
                bid_qty_.append(order_book_.bid_qty[i]);
                ask_qty_.append(order_book_.ask_qty[i]);
            }
            py_order_book["bid"] = bid_;
            py_order_book["ask"] = ask_;
            py_order_book["bid_qty"] = bid_qty_;
            py_order_book["ask_qty"] = ask_qty_;
            py_order_book["data_time"] = order_book_.data_time;
        }
        PyOnOrderBook(py_order_book);
    });
}

void MdApi::OnSubTickByTick(XTPST *ticker, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPST ticker_{};
    if (ticker) {
        has_data = true;
        ticker_ = *ticker;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker{};
        if (has_data) {
            py_ticker["exchange_id"] = ticker_.exchange_id;
            py_ticker["ticker"] = ticker_.ticker;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnSubTickByTick(py_ticker, py_error, is_last);
    });
}

void MdApi::OnUnSubTickByTick(XTPST *ticker, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPST ticker_{};
    if (ticker) {
        has_data = true;
        ticker_ = *ticker;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker{};
        if (has_data) {
            py_ticker["exchange_id"] = ticker_.exchange_id;
            py_ticker["ticker"] = ticker_.ticker;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnUnSubTickByTick(py_ticker, py_error, is_last);
    });
}

void MdApi::OnTickByTick(XTPTBT *tbt_data) {
    bool has_data{false};
    XTPTBT tbt_data_{};
    if (tbt_data) {
        has_data = true;
        tbt_data_ = *tbt_data;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_tbt_data{};
        if (has_data) {
            py_tbt_data["exchange_id"] = tbt_data_.exchange_id;
            py_tbt_data["ticker"] = tbt_data_.ticker;
            py_tbt_data["seq"] = tbt_data_.seq;
            py_tbt_data["data_time"] = tbt_data_.data_time;
            py_tbt_data["type"] = tbt_data_.type;
            switch (tbt_data_.type) {
                case XTP_TBT_ENTRUST:
                    py_tbt_data["channel_no"] = tbt_data_.entrust.channel_no;
                    py_tbt_data["seq"] = tbt_data_.entrust.seq;
                    py_tbt_data["price"] = tbt_data_.entrust.price;
                    py_tbt_data["qty"] = tbt_data_.entrust.qty;
                    py_tbt_data["side"] = tbt_data_.entrust.side;
                    py_tbt_data["ord_type"] = tbt_data_.entrust.ord_type;
                    py_tbt_data["order_no"] = tbt_data_.entrust.order_no;
                    break;
                case XTP_TBT_TRADE:
                    py_tbt_data["channel_no"] = tbt_data_.trade.channel_no;
                    py_tbt_data["seq"] = tbt_data_.trade.seq;
                    py_tbt_data["price"] = tbt_data_.trade.price;
                    py_tbt_data["qty"] = tbt_data_.trade.qty;
                    py_tbt_data["money"] = tbt_data_.trade.money;
                    py_tbt_data["bid_no"] = tbt_data_.trade.bid_no;
                    py_tbt_data["ask_no"] = tbt_data_.trade.ask_no;
                    py_tbt_data["trade_flag"] = tbt_data_.trade.trade_flag;
                    break;
                case XTP_TBT_STATE:
                    py_tbt_data["channel_no"] = tbt_data_.state.channel_no;
                    py_tbt_data["seq"] = tbt_data_.state.seq;
                    py_tbt_data["flag"] = tbt_data_.state.flag;
                    break;
                default:
                    break;
            }
        }
        PyOnTickByTick(py_tbt_data);
    });
}

void MdApi::OnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnSubscribeAllMarketData(exchange_id, py_error);
    });
}

void MdApi::OnUnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnUnSubscribeAllMarketData(exchange_id, py_error);
    });
}

void MdApi::OnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnSubscribeAllOrderBook(exchange_id, py_error);
    });
}

void MdApi::OnUnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnUnSubscribeAllOrderBook(exchange_id, py_error);
    });
}

void MdApi::OnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnSubscribeAllTickByTick(exchange_id, py_error);
    });
}

void MdApi::OnUnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnUnSubscribeAllTickByTick(exchange_id, py_error);
    });
}

void MdApi::OnQueryAllTickers(XTPQSI *ticker_info, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPQSI ticker_info_{};
    if (ticker_info) {
        has_data = true;
        ticker_info_ = *ticker_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker_info{};
        if (has_data) {
            py_ticker_info["exchange_id"] = ticker_info_.exchange_id;
            py_ticker_info["ticker"] = ticker_info_.ticker;
            py_ticker_info["ticker_name"] = ticker_info_.ticker_name;
            py_ticker_info["ticker_type"] = ticker_info_.ticker_type;
            py_ticker_info["pre_close_price"] = ticker_info_.pre_close_price;
            py_ticker_info["upper_limit_price"] = ticker_info_.upper_limit_price;
            py_ticker_info["lower_limit_price"] = ticker_info_.lower_limit_price;
            py_ticker_info["price_tick"] = ticker_info_.price_tick;
            py_ticker_info["buy_qty_unit"] = ticker_info_.buy_qty_unit;
            py_ticker_info["sell_qty_unit"] = ticker_info_.sell_qty_unit;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryAllTickers(py_ticker_info, py_error, is_last);
    });
}

void MdApi::OnQueryTickersPriceInfo(XTPTPI *ticker_info, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPTPI ticker_info_{};
    if (ticker_info) {
        has_data = true;
        ticker_info_ = *ticker_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker_info{};
        if (has_data) {
            py_ticker_info["exchange_id"] = ticker_info_.exchange_id;
            py_ticker_info["ticker"] = ticker_info_.ticker;
            py_ticker_info["last_price"] = ticker_info_.last_price;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryTickersPriceInfo(py_ticker_info, py_error, is_last);
    });
}

void MdApi::OnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnSubscribeAllOptionMarketData(exchange_id, py_error);
    });
}

void MdApi::OnUnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnUnSubscribeAllOptionMarketData(exchange_id, py_error);
    });
}

void MdApi::OnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnSubscribeAllOptionOrderBook(exchange_id, py_error);
    });
}

void MdApi::OnUnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnUnSubscribeAllOptionOrderBook(exchange_id, py_error);
    });
}

void MdApi::OnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnSubscribeAllOptionTickByTick(exchange_id, py_error);
    });
}

void MdApi::OnUnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnUnSubscribeAllOptionTickByTick(exchange_id, py_error);
    });
}

void MdApi::OnQueryAllTickersFullInfo(XTPQFI *ticker_info, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPQFI ticker_info_{};
    if (ticker_info) {
        has_data = true;
        ticker_info_ = *ticker_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker_info{};
        if (has_data) {
            py_ticker_info["exchange_id"] = ticker_info_.exchange_id;
            py_ticker_info["ticker"] = ticker_info_.ticker;
            py_ticker_info["ticker_name"] = ticker_info_.ticker_name;
            py_ticker_info["security_type"] = ticker_info_.security_type;
            py_ticker_info["ticker_qualification_class"] = ticker_info_.ticker_qualification_class;
            py_ticker_info["is_registration"] = ticker_info_.is_registration;
            py_ticker_info["is_VIE"] = ticker_info_.is_VIE;
            py_ticker_info["is_noprofit"] = ticker_info_.is_noprofit;
            py_ticker_info["is_weighted_voting_rights"] = ticker_info_.is_weighted_voting_rights;
            py_ticker_info["is_have_price_limit"] = ticker_info_.is_have_price_limit;
            py_ticker_info["upper_limit_price"] = ticker_info_.upper_limit_price;
            py_ticker_info["lower_limit_price"] = ticker_info_.lower_limit_price;
            py_ticker_info["pre_close_price"] = ticker_info_.pre_close_price;
            py_ticker_info["price_tick"] = ticker_info_.price_tick;
            py_ticker_info["bid_qty_upper_limit"] = ticker_info_.bid_qty_upper_limit;
            py_ticker_info["bid_qty_lower_limit"] = ticker_info_.bid_qty_lower_limit;
            py_ticker_info["bid_qty_unit"] = ticker_info_.bid_qty_unit;
            py_ticker_info["ask_qty_upper_limit"] = ticker_info_.ask_qty_upper_limit;
            py_ticker_info["ask_qty_lower_limit"] = ticker_info_.ask_qty_lower_limit;
            py_ticker_info["ask_qty_unit"] = ticker_info_.ask_qty_unit;
            py_ticker_info["market_bid_qty_upper_limit"] = ticker_info_.market_bid_qty_upper_limit;
            py_ticker_info["market_bid_qty_lower_limit"] = ticker_info_.market_bid_qty_lower_limit;
            py_ticker_info["market_bid_qty_unit"] = ticker_info_.market_bid_qty_unit;
            py_ticker_info["market_ask_qty_upper_limit"] = ticker_info_.market_ask_qty_upper_limit;
            py_ticker_info["market_ask_qty_lower_limit"] = ticker_info_.market_ask_qty_lower_limit;
            py_ticker_info["market_ask_qty_unit"] = ticker_info_.market_ask_qty_unit;
            py_ticker_info["security_status"] = ticker_info_.security_status;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryAllTickersFullInfo(py_ticker_info, py_error, is_last);
    });
}

void MdApi::OnQueryAllNQTickersFullInfo(XTPNQFI *ticker_info, XTPRI *error_info, bool is_last) {
    bool has_data{false};
    XTPNQFI ticker_info_{};
    if (ticker_info) {
        has_data = true;
        ticker_info_ = *ticker_info;
    }
    bool has_error{false};
    XTPRI error_{};
    if (error_info) {
        has_error = true;
        error_ = *error_info;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_ticker_info{};
        if (has_data) {
            py_ticker_info["exchange_id"] = ticker_info_.exchange_id;
            py_ticker_info["ticker"] = ticker_info_.ticker;
            py_ticker_info["ticker_name"] = ticker_info_.ticker_name;
            py_ticker_info["security_type"] = ticker_info_.security_type;
            py_ticker_info["ticker_qualification_class"] = ticker_info_.ticker_qualification_class;
            py_ticker_info["ticker_abbr_en"] = ticker_info_.ticker_abbr_en;
            py_ticker_info["base_ticker"] = ticker_info_.base_ticker;
            py_ticker_info["industry_type"] = ticker_info_.industry_type;
            py_ticker_info["currency_type"] = ticker_info_.currency_type;
            py_ticker_info["trade_unit"] = ticker_info_.trade_unit;
            py_ticker_info["hang_out_date"] = ticker_info_.hang_out_date;
            py_ticker_info["value_date"] = ticker_info_.value_date;
            py_ticker_info["maturity_date"] = ticker_info_.maturity_date;
            py_ticker_info["per_limit_vol"] = ticker_info_.per_limit_vol;
            py_ticker_info["buy_vol_unit"] = ticker_info_.buy_vol_unit;
            py_ticker_info["sell_vol_unit"] = ticker_info_.sell_vol_unit;
            py_ticker_info["mini_declared_vol"] = ticker_info_.mini_declared_vol;
            py_ticker_info["limit_price_attr"] = ticker_info_.limit_price_attr;
            py_ticker_info["market_maker_quantity"] = ticker_info_.market_maker_quantity;
            py_ticker_info["price_gear"] = ticker_info_.price_gear;
            py_ticker_info["first_limit_trans"] = ticker_info_.first_limit_trans;
            py_ticker_info["subsequent_limit_trans"] = ticker_info_.subsequent_limit_trans;
            py_ticker_info["limit_upper_price"] = ticker_info_.limit_upper_price;
            py_ticker_info["limit_lower_price"] = ticker_info_.limit_lower_price;
            py_ticker_info["block_trade_upper"] = ticker_info_.block_trade_upper;
            py_ticker_info["block_trade_lower"] = ticker_info_.block_trade_lower;
            py_ticker_info["convert_into_ration"] = ticker_info_.convert_into_ration;
            py_ticker_info["trade_status"] = ticker_info_.trade_status;
            py_ticker_info["security_level"] = ticker_info_.security_level;
            py_ticker_info["trade_type"] = ticker_info_.trade_type;
            py_ticker_info["suspend_flag"] = ticker_info_.suspend_flag;
            py_ticker_info["ex_dividend_flag"] = ticker_info_.ex_dividend_flag;
        }
        nb::dict py_error{};
        if (has_error) {
            py_error["error_id"] = error_.error_id;
            py_error["error_msg"] = error_.error_msg;
        }
        PyOnQueryAllNQTickersFullInfo(py_ticker_info, py_error, is_last);
    });
}

void MdApi::OnRebuildQuoteServerDisconnected(int reason) {
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        PyOnDisconnected(reason);
    });
}

void MdApi::OnRequestRebuildQuote(XTPQuoteRebuildResultRsp *rebuild_result) {
    bool has_data{false};
    XTPQuoteRebuildResultRsp rebuild_result_{};
    if (rebuild_result) {
        has_data = true;
        rebuild_result_ = *rebuild_result;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_rebuild_result{};
        if (has_data) {
            py_rebuild_result["request_id"] = rebuild_result_.request_id;
            py_rebuild_result["exchange_id"] = rebuild_result_.exchange_id;
            py_rebuild_result["size"] = rebuild_result_.size;
            py_rebuild_result["channel_number"] = rebuild_result_.channel_number;
            py_rebuild_result["begin"] = rebuild_result_.begin;
            py_rebuild_result["end"] = rebuild_result_.end;
            py_rebuild_result["result_code"] = rebuild_result_.result_code;
            py_rebuild_result["msg"] = rebuild_result_.msg;
        }
        PyOnRequestRebuildQuote(py_rebuild_result);
    });
}

void MdApi::OnRebuildTickByTick(XTPTBT *tbt_data) {
    bool has_data{false};
    XTPTBT tbt_data_{};
    if (tbt_data) {
        has_data = true;
        tbt_data_ = *tbt_data;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_tbt_data{};
        if (has_data) {
            py_tbt_data["exchange_id"] = tbt_data_.exchange_id;
            py_tbt_data["ticker"] = tbt_data_.ticker;
            py_tbt_data["ticker"] = tbt_data_.ticker;
            py_tbt_data["seq"] = tbt_data_.seq;
            py_tbt_data["data_time"] = tbt_data_.data_time;
            py_tbt_data["type"] = tbt_data_.type;
            switch (tbt_data_.type) {
                case XTP_TBT_ENTRUST:
                    py_tbt_data["channel_no"] = tbt_data_.entrust.channel_no;
                    py_tbt_data["seq"] = tbt_data_.entrust.seq;
                    py_tbt_data["price"] = tbt_data_.entrust.price;
                    py_tbt_data["qty"] = tbt_data_.entrust.qty;
                    py_tbt_data["side"] = tbt_data_.entrust.side;
                    py_tbt_data["ord_type"] = tbt_data_.entrust.ord_type;
                    py_tbt_data["order_no"] = tbt_data_.entrust.order_no;
                    break;
                case XTP_TBT_TRADE:
                    py_tbt_data["channel_no"] = tbt_data_.trade.channel_no;
                    py_tbt_data["seq"] = tbt_data_.trade.seq;
                    py_tbt_data["price"] = tbt_data_.trade.price;
                    py_tbt_data["qty"] = tbt_data_.trade.qty;
                    py_tbt_data["money"] = tbt_data_.trade.money;
                    py_tbt_data["bid_no"] = tbt_data_.trade.bid_no;
                    py_tbt_data["ask_no"] = tbt_data_.trade.ask_no;
                    py_tbt_data["trade_flag"] = tbt_data_.trade.trade_flag;
                    break;
                case XTP_TBT_STATE:
                    py_tbt_data["channel_no"] = tbt_data_.state.channel_no;
                    py_tbt_data["seq"] = tbt_data_.state.seq;
                    py_tbt_data["flag"] = tbt_data_.state.flag;
                    break;
                default:
                    break;
            }
        }
        PyOnRebuildTickByTick(py_tbt_data);
    });
}

void MdApi::OnRebuildMarketData(XTPMD *md_data) {
    bool has_data{false};
    XTPMD md_data_{};
    if (md_data) {
        has_data = true;
        md_data_ = *md_data;
    }
    queue_->dispatch([=]() {
        nb::gil_scoped_acquire acquire;
        nb::dict py_md_data{};
        if (has_data) {
            py_md_data["exchange_id"] = md_data_.exchange_id;
            py_md_data["ticker"] = md_data_.ticker;
            py_md_data["last_price"] = md_data_.last_price;
            py_md_data["pre_close_price"] = md_data_.pre_close_price;
            py_md_data["open_price"] = md_data_.open_price;
            py_md_data["high_price"] = md_data_.high_price;
            py_md_data["low_price"] = md_data_.low_price;
            py_md_data["close_price"] = md_data_.close_price;
            py_md_data["pre_total_long_positon"] = md_data_.pre_total_long_positon;
            py_md_data["total_long_positon"] = md_data_.total_long_positon;
            py_md_data["pre_settl_price"] = md_data_.pre_settl_price;
            py_md_data["settl_price"] = md_data_.settl_price;
            py_md_data["upper_limit_price"] = md_data_.upper_limit_price;
            py_md_data["lower_limit_price"] = md_data_.lower_limit_price;
            py_md_data["pre_delta"] = md_data_.pre_delta;
            py_md_data["curr_delta"] = md_data_.curr_delta;
            py_md_data["data_time"] = md_data_.data_time;
            py_md_data["qty"] = md_data_.qty;
            py_md_data["turnover"] = md_data_.turnover;
            py_md_data["avg_price"] = md_data_.avg_price;

            nb::list bid_{};
            nb::list ask_{};
            nb::list bid_qty_{};
            nb::list ask_qty_{};
            for (int i = 0; i < 10; i++) {
                bid_.append(md_data_.bid[i]);
                ask_.append(md_data_.ask[i]);
                bid_qty_.append(md_data_.bid_qty[i]);
                ask_qty_.append(md_data_.ask_qty[i]);
            }
            py_md_data["bid"] = bid_;
            py_md_data["ask"] = ask_;
            py_md_data["bid_qty"] = bid_qty_;
            py_md_data["ask_qty"] = ask_qty_;

            py_md_data["trades_count"] = md_data_.trades_count;
            py_md_data["ticker_status"] = md_data_.ticker_status;

            switch (md_data_.data_type_v2) {
                case XTP_MARKETDATA_V2_ACTUAL:
                    py_md_data["total_bid_qty"] = md_data_.stk.total_bid_qty;
                    py_md_data["total_ask_qty"] = md_data_.stk.total_ask_qty;
                    py_md_data["ma_bid_price"] = md_data_.stk.ma_bid_price;
                    py_md_data["ma_ask_price"] = md_data_.stk.ma_ask_price;
                    py_md_data["ma_bond_bid_price"] = md_data_.stk.ma_bond_bid_price;
                    py_md_data["ma_bond_ask_price"] = md_data_.stk.ma_bond_ask_price;
                    py_md_data["yield_to_maturity"] = md_data_.stk.yield_to_maturity;
                    py_md_data["iopv"] = md_data_.stk.iopv;
                    py_md_data["etf_buy_count"] = md_data_.stk.etf_buy_count;
                    py_md_data["etf_sell_count"] = md_data_.stk.etf_sell_count;
                    py_md_data["etf_buy_qty"] = md_data_.stk.etf_buy_qty;
                    py_md_data["etf_buy_money"] = md_data_.stk.etf_buy_money;
                    py_md_data["etf_sell_money"] = md_data_.stk.etf_sell_money;
                    py_md_data["total_warrant_exec_qty"] = md_data_.stk.total_warrant_exec_qty;
                    py_md_data["warrant_lower_price"] = md_data_.stk.warrant_lower_price;
                    py_md_data["warrant_upper_price"] = md_data_.stk.warrant_upper_price;
                    py_md_data["cancel_buy_count"] = md_data_.stk.cancel_buy_count;
                    py_md_data["cancel_sell_count"] = md_data_.stk.cancel_sell_count;
                    py_md_data["cancel_buy_qty"] = md_data_.stk.cancel_buy_qty;
                    py_md_data["cancel_sell_qty"] = md_data_.stk.cancel_sell_qty;
                    py_md_data["cancel_buy_money"] = md_data_.stk.cancel_buy_money;
                    py_md_data["cancel_sell_money"] = md_data_.stk.cancel_sell_money;
                    py_md_data["total_buy_count"] = md_data_.stk.total_buy_count;
                    py_md_data["total_sell_count"] = md_data_.stk.total_sell_count;
                    py_md_data["duration_after_buy"] = md_data_.stk.duration_after_buy;
                    py_md_data["duration_after_sell"] = md_data_.stk.duration_after_sell;
                    py_md_data["num_bid_orders"] = md_data_.stk.num_bid_orders;
                    py_md_data["num_ask_orders"] = md_data_.stk.num_ask_orders;
                    py_md_data["pre_iopv"] = md_data_.stk.pre_iopv;
                    py_md_data["r1"] = md_data_.stk.r1;
                    py_md_data["r2"] = md_data_.stk.r2;
                    break;
                case XTP_MARKETDATA_V2_OPTION:
                    py_md_data["auction_price"] = md_data_.opt.auction_price;
                    py_md_data["auction_qty"] = md_data_.opt.auction_qty;
                    py_md_data["last_enquiry_time"] = md_data_.opt.last_enquiry_time;
                    break;
                case XTP_MARKETDATA_V2_BOND:
                    py_md_data["total_bid_qty"] = md_data_.bond.total_bid_qty;
                    py_md_data["total_ask_qty"] = md_data_.bond.total_ask_qty;
                    py_md_data["ma_bid_price"] = md_data_.bond.ma_bid_price;
                    py_md_data["ma_ask_price"] = md_data_.bond.ma_ask_price;
                    py_md_data["ma_bond_bid_price"] = md_data_.bond.ma_bond_bid_price;
                    py_md_data["ma_bond_ask_price"] = md_data_.bond.ma_bond_ask_price;
                    py_md_data["yield_to_maturity"] = md_data_.bond.yield_to_maturity;
                    py_md_data["match_lastpx"] = md_data_.bond.match_lastpx;
                    py_md_data["ma_bond_price"] = md_data_.bond.ma_bond_price;
                    py_md_data["match_qty"] = md_data_.bond.match_qty;
                    py_md_data["match_turnover"] = md_data_.bond.match_turnover;
                    py_md_data["r4"] = md_data_.bond.r4;
                    py_md_data["r5"] = md_data_.bond.r5;
                    py_md_data["r6"] = md_data_.bond.r6;
                    py_md_data["r7"] = md_data_.bond.r7;
                    py_md_data["r8"] = md_data_.bond.r8;
                    py_md_data["cancel_buy_count"] = md_data_.bond.cancel_buy_count;
                    py_md_data["cancel_sell_count"] = md_data_.bond.cancel_sell_count;
                    py_md_data["cancel_buy_qty"] = md_data_.bond.cancel_buy_qty;
                    py_md_data["cancel_sell_qty"] = md_data_.bond.cancel_sell_qty;
                    py_md_data["cancel_buy_money"] = md_data_.bond.cancel_buy_money;
                    py_md_data["cancel_sell_money"] = md_data_.bond.cancel_sell_money;
                    py_md_data["total_buy_count"] = md_data_.bond.total_buy_count;
                    py_md_data["total_sell_count"] = md_data_.bond.total_sell_count;
                    py_md_data["duration_after_buy"] = md_data_.bond.duration_after_buy;
                    py_md_data["duration_after_sell"] = md_data_.bond.duration_after_sell;
                    py_md_data["num_bid_orders"] = md_data_.bond.num_bid_orders;
                    py_md_data["num_ask_orders"] = md_data_.bond.num_ask_orders;
                    py_md_data["instrument_status"] = md_data_.bond.instrument_status;
                    break;
                default:
                    break;
            }

            py_md_data["data_type"] = md_data_.data_type;
            py_md_data["data_type_v2"] = md_data_.data_type_v2;
        }
        PyOnRebuildMarketData(py_md_data);
    });
}
