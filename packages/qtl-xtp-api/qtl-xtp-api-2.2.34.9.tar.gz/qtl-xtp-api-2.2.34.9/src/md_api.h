#ifndef MD_API_H
#define MD_API_H

#include <iostream>
#include <string>
#include <vector>
#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>
#include <nanobind/trampoline.h>

#include "utils.h"
#include "dispatch_queue.h"
#include "xtp_quote_api.h"


namespace nb = nanobind;
namespace xtp = XTP::API;


class MdApi : public xtp::QuoteSpi {
private:
    std::unique_ptr<DispatchQueue> queue_;
    xtp::QuoteApi *api_;

public:
    void CreateQuoteApi(int client_id, const std::string &save_file_path, int log_level);
    void Destroy();
    std::string GetTradingDay();
    std::string GetApiVersion();
    nb::dict GetApiLastError();
    void SetUDPBufferSize(uint32_t buff_size);
    void SetHeartBeatInterval(uint32_t interval);
    void SetUDPRecvThreadAffinity(int32_t cpu_no);
    void SetUDPRecvThreadAffinityArray(const std::vector<int32_t> &cpu_no_array);
    void SetUDPParseThreadAffinity(int32_t cpu_no);
    void SetUDPParseThreadAffinityArray(const std::vector<int32_t> &cpu_no_array);
    void SetUDPSeqLogOutPutFlag(bool flag = true);
    int SubscribeMarketData(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id);
    int UnSubscribeMarketData(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id);
    int SubscribeOrderBook(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id);
    int UnSubscribeOrderBook(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id);
    int SubscribeTickByTick(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id);
    int UnSubscribeTickByTick(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id);
    int SubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int UnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int SubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int UnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int SubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int UnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int Login(const char *ip, int port, const char *user, const char *password, XTP_PROTOCOL_TYPE sock_type,
              const char *local_ip = nullptr);
    int Logout();

    int QueryAllTickers(XTP_EXCHANGE_TYPE exchange_id);
    int QueryTickersPriceInfo(const std::vector<std::string> &ticker, XTP_EXCHANGE_TYPE exchange_id);
    int QueryAllTickersPriceInfo();

    int SubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int UnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int SubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int UnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int SubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);
    int UnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id = XTP_EXCHANGE_UNKNOWN);

    int QueryAllTickersFullInfo(XTP_EXCHANGE_TYPE exchange_id);
    int QueryAllNQTickersFullInfo();

    int LoginToRebuildQuoteServer(const char *ip, int port, const char *user, const char *password,
                                  XTP_PROTOCOL_TYPE sock_type, const char *local_ip = nullptr);
    int LogoutFromRebuildQuoteServer();

    int RequestRebuildQuote(const nb::dict &rebuild_param);

    void OnDisconnected(int reason) override;
    void OnError(XTPRI *error_info) override;
    void OnSubMarketData(XTPST *ticker, XTPRI *error_info, bool is_last) override;
    void OnUnSubMarketData(XTPST *ticker, XTPRI *error_info, bool is_last) override;
    void OnDepthMarketData(XTPMD *market_data, int64_t bid1_qty[], int32_t bid1_count, int32_t max_bid1_count,
                           int64_t ask1_qty[], int32_t ask1_count, int32_t max_ask1_count) override;
    void OnSubOrderBook(XTPST *ticker, XTPRI *error_info, bool is_last) override;
    void OnUnSubOrderBook(XTPST *ticker, XTPRI *error_info, bool is_last) override;
    void OnOrderBook(XTPOB *order_book) override;
    void OnSubTickByTick(XTPST *ticker, XTPRI *error_info, bool is_last) override;
    void OnUnSubTickByTick(XTPST *ticker, XTPRI *error_info, bool is_last) override;
    void OnTickByTick(XTPTBT *tbt_data) override;
    void OnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnUnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnUnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnUnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnQueryAllTickers(XTPQSI *ticker_info, XTPRI *error_info, bool is_last) override;
    void OnQueryTickersPriceInfo(XTPTPI *ticker_info, XTPRI *error_info, bool is_last) override;
    void OnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnUnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnUnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnUnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;
    void OnQueryAllTickersFullInfo(XTPQFI *ticker_info, XTPRI *error_info, bool is_last) override;
    void OnQueryAllNQTickersFullInfo(XTPNQFI *ticker_info, XTPRI *error_info, bool is_last) override;
    void OnRebuildQuoteServerDisconnected(int reason) override;
    void OnRequestRebuildQuote(XTPQuoteRebuildResultRsp *rebuild_result) override;
    void OnRebuildTickByTick(XTPTBT *tbt_data) override;
    void OnRebuildMarketData(XTPMD *md_data) override;

    virtual void PyOnDisconnected(int reason) = 0;
    virtual void PyOnError(const nb::dict &error_info) = 0;
    virtual void PyOnSubMarketData(const nb::dict &ticker, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnUnSubMarketData(const nb::dict &ticker, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnDepthMarketData(const nb::dict &market_data, const std::vector<int64_t> &bid1_qty, int32_t max_bid1_count,
                                     const std::vector<int64_t> &ask1_qty, int32_t max_ask1_count) = 0;
    virtual void PyOnSubOrderBook(const nb::dict &ticker, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnUnSubOrderBook(const nb::dict &ticker, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnOrderBook(const nb::dict &order_book) = 0;
    virtual void PyOnSubTickByTick(const nb::dict &ticker, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnUnSubTickByTick(const nb::dict &ticker, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnTickByTick(const nb::dict &tbt_data) = 0;
    virtual void PyOnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnUnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnUnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnUnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnQueryAllTickers(const nb::dict &ticker_info, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnQueryTickersPriceInfo(const nb::dict &ticker_info, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnUnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnUnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnUnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) = 0;
    virtual void PyOnQueryAllTickersFullInfo(const nb::dict &ticker_info, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnQueryAllNQTickersFullInfo(const nb::dict &ticker_info, const nb::dict &error_info, bool is_last) = 0;
    virtual void PyOnRebuildQuoteServerDisconnected(int reason) = 0;
    virtual void PyOnRequestRebuildQuote(const nb::dict &rebuild_result) = 0;
    virtual void PyOnRebuildTickByTick(const nb::dict &tbt_data) = 0;
    virtual void PyOnRebuildMarketData(const nb::dict &md_data) = 0;
};


class PyMdApi final : public MdApi {
public:
    NB_TRAMPOLINE(MdApi, 31);

    void PyOnDisconnected(int reason) override {
        NB_OVERRIDE_PURE_NAME(
                "OnDisconnected",
                PyOnDisconnected,
                reason
        );
    }

    void PyOnError(const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnError",
                PyOnError,
                error_info
        );
    }

    void PyOnSubMarketData(const nb::dict &ticker, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnSubMarketData",
                PyOnSubMarketData,
                ticker,
                error_info,
                is_last
        );
    }

    void PyOnUnSubMarketData(const nb::dict &ticker, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnUnSubMarketData",
                PyOnUnSubMarketData,
                ticker,
                error_info,
                is_last
        );
    }

    void PyOnDepthMarketData(const nb::dict &market_data, const std::vector<int64_t> &bid1_qty, int32_t max_bid1_count,
                             const std::vector<int64_t> &ask1_qty, int32_t max_ask1_count) override {
        NB_OVERRIDE_PURE_NAME(
                "OnDepthMarketData",
                PyOnDepthMarketData,
                market_data,
                bid1_qty,
                max_bid1_count,
                ask1_qty,
                max_ask1_count
        );
    }

    void PyOnSubOrderBook(const nb::dict &ticker, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnSubOrderBook",
                PyOnSubOrderBook,
                ticker,
                error_info,
                is_last
        );
    }

    void PyOnUnSubOrderBook(const nb::dict &ticker, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnUnSubOrderBook",
                PyOnUnSubOrderBook,
                ticker,
                error_info,
                is_last
        );
    }

    void PyOnOrderBook(const nb::dict &order_book) override {
        NB_OVERRIDE_PURE_NAME(
                "OnOrderBook",
                PyOnOrderBook,
                order_book
        );
    }

    void PyOnSubTickByTick(const nb::dict &ticker, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnSubTickByTick",
                PyOnSubTickByTick,
                ticker,
                error_info,
                is_last
        );
    }

    void PyOnUnSubTickByTick(const nb::dict &ticker, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnUnSubTickByTick",
                PyOnUnSubTickByTick,
                ticker,
                error_info,
                is_last
        );
    }

    void PyOnTickByTick(const nb::dict &tbt_data) override {
        NB_OVERRIDE_PURE_NAME(
                "OnTickByTick",
                PyOnTickByTick,
                tbt_data
        );
    }

    void PyOnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnSubscribeAllMarketData",
                PyOnSubscribeAllMarketData,
                exchange_id,
                error_info
        );
    }

    void PyOnUnSubscribeAllMarketData(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnUnSubscribeAllMarketData",
                PyOnUnSubscribeAllMarketData,
                exchange_id,
                error_info
        );
    }

    void PyOnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnSubscribeAllOrderBook",
                PyOnSubscribeAllOrderBook,
                exchange_id,
                error_info
        );
    }

    void PyOnUnSubscribeAllOrderBook(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnUnSubscribeAllOrderBook",
                PyOnUnSubscribeAllOrderBook,
                exchange_id,
                error_info
        );
    }

    void PyOnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnSubscribeAllTickByTick",
                PyOnSubscribeAllTickByTick,
                exchange_id,
                error_info
        );
    }

    void PyOnUnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnUnSubscribeAllTickByTick",
                PyOnUnSubscribeAllTickByTick,
                exchange_id,
                error_info
        );
    }

    void PyOnQueryAllTickers(const nb::dict &ticker_info, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryAllTickers",
                PyOnQueryAllTickers,
                ticker_info,
                error_info,
                is_last
        );
    }

    void PyOnQueryTickersPriceInfo(const nb::dict &ticker_info, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryTickersPriceInfo",
                PyOnQueryTickersPriceInfo,
                ticker_info,
                error_info,
                is_last
        );
    }

    void PyOnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnSubscribeAllOptionMarketData",
                PyOnSubscribeAllOptionMarketData,
                exchange_id,
                error_info
        );
    }

    void PyOnUnSubscribeAllOptionMarketData(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnUnSubscribeAllOptionMarketData",
                PyOnUnSubscribeAllOptionMarketData,
                exchange_id,
                error_info
        );
    }

    void PyOnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnSubscribeAllOptionOrderBook",
                PyOnSubscribeAllOptionOrderBook,
                exchange_id,
                error_info
        );
    }

    void PyOnUnSubscribeAllOptionOrderBook(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnUnSubscribeAllOptionOrderBook",
                PyOnUnSubscribeAllOptionOrderBook,
                exchange_id,
                error_info
        );
    }

    void PyOnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnSubscribeAllOptionTickByTick",
                PyOnSubscribeAllOptionTickByTick,
                exchange_id,
                error_info
        );
    }

    void PyOnUnSubscribeAllOptionTickByTick(XTP_EXCHANGE_TYPE exchange_id, const nb::dict &error_info) override {
        NB_OVERRIDE_PURE_NAME(
                "OnUnSubscribeAllOptionTickByTick",
                PyOnUnSubscribeAllOptionTickByTick,
                exchange_id,
                error_info
        );
    }

    void PyOnQueryAllTickersFullInfo(const nb::dict &ticker_info, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryAllTickersFullInfo",
                PyOnQueryAllTickersFullInfo,
                ticker_info,
                error_info,
                is_last
        );
    }

    void PyOnQueryAllNQTickersFullInfo(const nb::dict &ticker_info, const nb::dict &error_info, bool is_last) override {
        NB_OVERRIDE_PURE_NAME(
                "OnQueryAllNQTickersFullInfo",
                PyOnQueryAllNQTickersFullInfo,
                ticker_info,
                error_info,
                is_last
        );
    }

    void PyOnRebuildQuoteServerDisconnected(int reason) override {
        NB_OVERRIDE_PURE_NAME(
                "OnRebuildQuoteServerDisconnected",
                PyOnRebuildQuoteServerDisconnected,
                reason
        );
    }

    void PyOnRequestRebuildQuote(const nb::dict &rebuild_result) override {
        NB_OVERRIDE_PURE_NAME(
                "OnRequestRebuildQuote",
                PyOnRequestRebuildQuote,
                rebuild_result
        );
    }

    void PyOnRebuildTickByTick(const nb::dict &tbt_data) override {
        NB_OVERRIDE_PURE_NAME(
                "OnRebuildTickByTick",
                PyOnRebuildTickByTick,
                tbt_data
        );
    }

    void PyOnRebuildMarketData(const nb::dict &md_data) override {
        NB_OVERRIDE_PURE_NAME(
                "OnRebuildMarketData",
                PyOnRebuildMarketData,
                md_data
        );
    }
};

#endif //MD_API_H
