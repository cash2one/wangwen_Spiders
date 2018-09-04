!function() {
    function e(e, o, a) {
        var n = {
            moduleIds: e,
            timestamp: public.timestamp,
            sign: md5(e + public.timestamp + public.pageKey)
        };
        $.ajax({
            type: "POST",
            url: public.ajaxUrl + "?r=pcapi/pcpage/moduleinfo",
            data: n
        }).done(function(n) {
            var i = !1;
            try {
                i = JSON.parse(n),
                console.log("榜单信息"),
                console.log(i)
            } catch (e) {}
            if (200 == i.state) {
                var r, c = i.data["module" + e];
                0 == a ? (r = _.template($("#bk_bd_tpl").html()),
                $("#coverbd").html(r({
                    data: c,
                    title: o
                })),
                $("#coverbd").seamless({
                    direction: "right",
                    step: 6
                })) : 1 == a && (r = _.template($("#bk_rbd_tpl").html()),
                $("#js_coverrbdbox").html(r({
                    data: c,
                    title: o
                })),
                t())
            }
            public.defaulImg()
        }).fail(function(e, t, o) {}).always(function() {
            count++,
            4 == count && (console.log(count),
            "function" == typeof window.callPhantom && window.callPhantom())
        })
    }
    function t() {
        var e = $(".cover-rbdbox").find("dl")
          , t = null;
        e.eq(0).find(".cover-rtdd").addClass("cover-active"),
        e.eq(0).find(".cover-rcdd").removeClass("cover-active");
        for (var o = 0, a = e.length; o < a; o++)
            e[o].index = o,
            $(e[o]).on("mouseenter", function() {
                clearTimeout(t);
                var o = this;
                t = setTimeout(function() {
                    for (var t = 0, a = e.length; t < a; t++)
                        $(e[t]).find(".cover-rtdd").removeClass("cover-active"),
                        $(e[t]).find(".cover-rcdd").addClass("cover-active");
                    $(e[o.index]).find(".cover-rtdd").addClass("cover-active"),
                    $(e[o.index]).find(".cover-rcdd").removeClass("cover-active")
                }, 400)
            })
    }
    function o() {
        var e = readCookie()
          , t = e.getBook() || null
          , o = public.queryString().bid;
        ajaxUrl = public.ajaxUrl + "?r=pcapi/pcbook/bookinfo",
        queryData = {
            bid: o,
            timestamp: public.timestamp,
            sign: md5(o + public.timestamp + public.bookKey)
        },
        $.ajax({
            type: "POST",
            url: ajaxUrl,
            data: queryData
        }).done(function(i) {
            var r = !1;
            try {
                r = JSON.parse(i),
                console.log("书籍数据"),
                console.log(r),
                authorName_cover = r.data.author_name,
                authorId_cover = r.data.sqAuthorId,
                bookName_cover = r.data.book_name,
                bookId_cover = r.data.sqBid,
                r.data.sqBid || $(".cannot-comment-cover").removeClass("hide")
            } catch (e) {}
            if (200 == r.state) {
                var c = r.data
                  , d = r.like;
                if (2 == r.data.hide)
                    return $(".down-shelf").removeClass("hide"),
                    $(".cca-all-comment").hide(),
                    void setTimeout(function() {
                        $(".cca-all-comment").show(),
                        $(".down-shelf").addClass("hide"),
                        window.location.href = "/"
                    }, 3e3);
                console.log("########", c);
                var s = _.template($("#bk_inof_tpl").html());
                $(".covertbox").html(s({
                    data: c
                })),
                l();
                var m = _.template($("#bk_chr_tpl").html());
                if ($(".bknewc").html(m({
                    data: c
                })),
                d.length) {
                    var p = _.template($("#bk_liek_tpl").html());
                    $("#liekbox").html(p({
                        data: d
                    }))
                }
                $("#liekbox").seamless({
                    direction: "right",
                    step: 6
                }),
                public.defaulImg(),
                n(),
                a();
                for (var u in t)
                    if (t[u].bid == o) {
                        if ($(".addbksj").addClass("yiadd").html("已加入书架").off(),
                        t[u].cid) {
                            $(".goread").html("继续阅读");
                            var g = "./read.php?bid=" + encodeReading(t[u].bid) + "&chapid=" + encodeReading(t[u].cid) + "&sqbid=" + $(".goread").attr("data-sqbid");
                            $(".goread").attr("href", g)
                        }
                        return !1
                    }
                $(".addbksj").on("click", function(t) {
                    var o = {
                        bid: c.bid,
                        title: c.book_name,
                        cover: c.cover,
                        end: c.end,
                        yidu: c.fristChapName,
                        cid: c.fristChapid,
                        newc: c.newChapName,
                        aut: c.author_name,
                        time: (new Date).getTime()
                    };
                    return e.addBook(o),
                    $(this).addClass("yiadd").html("已加入书架").off(),
                    t.preventDefault(),
                    !1
                })
            }
        }).fail(function(e, t, o) {}).always(function() {
            count++,
            4 == count && (console.log(count),
            "function" == typeof window.callPhantom && window.callPhantom())
        })
    }
    function a() {
        var e = ~~((new Date).getTime() / 1e3);
        $.ajax({
            url: APIUrl + "appapi/ppuser/ppuser_check_bind_business.php",
            data: {
                userId: localStorage.userId,
                type: 1,
                businessId: authorId_cover,
                timestamp: e,
                key: md5("c56cf32e9a52a265ae47cd50570266cc" + e)
            },
            type: "POST",
            success: function(e) {
                console.log("判断是否是作者"),
                e = JSON.parse(e),
                console.log(e),
                200 == e.status ? e.data.isBind && (window.isWriter = !0) : console.log(e.message),
                c(bookId_cover, authorId_cover),
                d(bookId_cover, authorId_cover)
            }
        })
    }
    function n() {
        var e = $(".text-comment-cover-input-login")
          , t = $(".text-comment-cover-input")
          , o = $(".text-comment-cover-textarea")
          , a = $(".text-comment-cover-textarea-textarea")
          , n = $(".text-comment-cover-textarea-div-comment-btn")
          , r = $(".text-comment-cover-textarea-div-comment-btn-cancel")
          , c = $(".text-comment-cover-textarea-div-now-num")
          , d = $(".text-comment-cover-denglu")
          , l = $(".text-comment-cover-zhuce");
        localStorage.userId ? (e.addClass("hide"),
        t.removeClass("hide"),
        t.unbind("click").bind("click", function() {
            $(document).trigger("commentOpen")
        }),
        a.bind("input", function(e) {
            c.text($(this).val().length)
        }),
        n.unbind("click").bind("click", function() {
            i()
        }),
        r.unbind("click").bind("click", function() {
            $(document).trigger("commentClose")
        }),
        $(document).bind("commentOpen", function() {
            t.addClass("hide"),
            o.removeClass("hide"),
            a.focus()
        }),
        $(document).bind("commentClose", function() {
            t.removeClass("hide"),
            o.addClass("hide")
        })) : (e.removeClass("hide"),
        d.unbind("click").bind("click", function() {
            $("#login").dialog("open")
        }),
        l.unbind("click").bind("click", function() {
            window.location.href = "./sign.php"
        }))
    }
    function i() {
        if (window.timeLimit) {
            if (window.timeLimit = !1,
            setTimeout(function() {
                window.timeLimit = !0
            }, 1e3),
            !bookId_cover)
                return void messageAlert("warning", "此书暂不可评论");
            var e = $(".text-comment-cover-textarea-textarea").val()
              , t = ~~((new Date).getTime() / 1e3)
              , o = "sq_uid=" + localStorage.userId + "&sn=" + window.FingerprintCode + "&imei=" + window.FingerprintCode + "&appid=10000&app_time=" + t + "&key=" + sessionStorage.keyParams
              , a = md5(o).toString().toUpperCase();
            return e = r(e),
            e.length < 5 || e.length > 500 ? void messageAlert("warning", "评论字数要求5~500个字范围内。") : void $.ajax({
                url: window.comment_url + "novel/i.php?do=sp_pub",
                data: {
                    appSignParms: "sq_uid:sn:imei:appid:app_time",
                    app_time: t,
                    authorId: authorId_cover,
                    authorName: authorName_cover,
                    bookId: bookId_cover,
                    bookName: bookName_cover,
                    imei: window.FingerprintCode,
                    sign: a,
                    sn: window.FingerprintCode,
                    source: "store",
                    sqUid: localStorage.userId || 8e6,
                    text: e
                },
                type: "POST",
                success: function(t) {
                    console.log("发表评论"),
                    console.log(t);
                    var o = "http://tp2.sinaimg.cn/5885514945/50/0/1";
                    if (200 == t.status) {
                        $(".text-comment-cover-textarea-textarea").val(""),
                        $(document).trigger("commentClose"),
                        t.info.userInfos[localStorage.userId].userPhoto && (o = t.info.userInfos[localStorage.userId].userPhoto);
                        var a = _.template($("#cca-comment-publish").html());
                        $(".cca-div-out").prepend(emotionPos()(a({
                            name: localStorage.nickname,
                            text: e,
                            mid: t.data.mid,
                            thisWriter: window.isWriter,
                            img: o
                        }))),
                        $(".nobody-comment-cover").addClass("hide"),
                        messageAlert("warning", "评论发表成功")
                    } else
                        "10008" == t.status && $("#login").dialog("open"),
                        messageAlert("warning", t.message)
                }
            })
        }
    }
    function r(e) {
        return null == e ? "" : e.replace(/\</g, "&lt;").replace(/\>/g, "&gt;")
    }
    function c(e, t) {
        $.ajax({
            url: window.comment_url + "novel/i.php?do=sp_get",
            data: {
                authorId: t,
                bookId: e,
                fetch: "merge",
                source: "store",
                sqUid: localStorage.userId || 8e6
            },
            type: "GET",
            success: function(e) {
                if (console.log("书评数据"),
                console.log(e),
                "21509" == e.status && $(".nobody-comment-cover").removeClass("hide"),
                200 == e.status) {
                    $(".title-comment-cover-right-span").html(e.info.total),
                    e.info.total > 10 && $(".cca-l-more").removeClass("hide");
                    var t = e.data.length > 5 ? e.data.slice(0, 5) : e.data
                      , o = _.template($("#cca-comment-l").html());
                    $(".cca-div-out").html(emotionPos()(o({
                        data: t,
                        thisWriter: window.isWriter,
                        ding: !1
                    })))
                }
            }
        })
    }
    function d(e, t) {
        $.ajax({
            url: window.comment_url + "novel/i.php?do=sp_get",
            data: {
                authorId: t,
                bookId: e,
                fetch: "top",
                source: "store",
                sqUid: localStorage.userId || 8e6
            },
            type: "GET",
            success: function(e) {
                if (console.log("置顶书评数据"),
                console.log(e),
                "21509" == e.status && (window.enableDing = !0,
                $(".cca-div-out-ding").html("")),
                200 == e.status) {
                    var t = _.template($("#cca-comment-l").html());
                    $(".cca-div-out-ding").html(emotionPos()(t({
                        data: e.data.slice(0, 1),
                        thisWriter: window.isWriter,
                        ding: !0
                    })))
                } else
                    $(".cca-div-out-ding").html("")
            }
        })
    }
    function l() {
        var e = 120
          , t = $(".part")
          , o = $(".all")
          , a = t.html().length;
        a > e && t.html(t.html().substring(0, e) + '...<a class="zk" href="#"></a>'),
        $(".zk").on("click", function() {
            return t.hide(),
            o.show(),
            !1
        }),
        $(".sq").on("click", function() {
            t.show(),
            o.hide()
        })
    }
    function s(e) {
        var t = 2;
        $.ajax({
            type: "POST",
            url: public.ajaxUrl + "?r=pcapi/pcpage/pageinfo",
            data: {
                pageId: t,
                timestamp: public.timestamp,
                sign: md5(t + public.timestamp + public.pageKey)
            }
        }).done(function(t) {
            var o = !1;
            try {
                console.log("榜单初始信息"),
                o = JSON.parse(t),
                console.log(o)
            } catch (e) {}
            200 == o.state && "function" == typeof e && e(o.data)
        }).fail(function(e, t, o) {}).always(function() {
            count++,
            4 == count && (console.log(count),
            "function" == typeof window.callPhantom && window.callPhantom())
        })
    }
    PV("封面页"),
    $(function() {
        function t(e, t, o, a) {
            var n = {
                authorId: authorId_cover,
                mid: t,
                sqUid: localStorage.userId || 8e6
            };
            "book-reply" == o ? (n.page = 1,
            n.size = 10) : (n.page = 1,
            n.size = 200),
            $.ajax({
                url: window.comment_url + "novel/i.php?do=sp_info",
                data: n,
                type: "GET",
                success: function(t) {
                    if (200 == t.status)
                        if ("book-reply" == o) {
                            var n = _.template($("#bk_sp_info_tpl").html());
                            e.find(".user-reply-box").html(n({
                                data: t.data,
                                info: t.info
                            }))
                        } else {
                            if ($(e).children().length > 1)
                                return;
                            var n = _.template($("#bk_sp_author_tpl").html());
                            $(e).append(n({
                                replyAuthor: a,
                                data: t.data
                            }))
                        }
                }
            })
        }
        window.authorName_cover,
        window.authorId_cover,
        window.bookName_cover,
        window.bookId_cover,
        window.count = 0,
        window.isWriter = !1,
        window.timeLimit = !0,
        window.enableDing = !1,
        $(document).on("click", ".tmall-activity", function() {
            setTimeout(function() {
                window.location.href = "/shiyue.php"
            }, 300)
        });
        var a = $(".cca-all-comment");
        a.on("click", ".cca-opera-zan", function(e) {
            var t = $(e.currentTarget)
              , o = t.attr("mid")
              , a = (new Date).getTime() % 1e7 + 1e8;
            if (!t.hasClass("cca-zan")) {
                t.addClass("cca-zan"),
                localStorage.zan ? localStorage.zan = localStorage.zan + t.attr("mid") : localStorage.zan = t.attr("mid");
                var n = t.find(".cca-zan-num").html();
                t.find(".cca-zan-num").html(parseInt(n) + 1);
                var i = t.find(".zan-donghua");
                i.animate({
                    top: "-7px",
                    opacity: "1"
                }, 300),
                i.animate({
                    top: "-15px",
                    opacity: "0"
                }, 300),
                $.ajax({
                    url: window.comment_url + "novel/i.php?do=sp_zan",
                    data: {
                        sqUid: localStorage.userId || a,
                        mid: o
                    },
                    type: "GET",
                    success: function(e) {
                        console.log("点赞"),
                        console.log(e)
                    }
                })
            }
        }),
        a.on("click", ".cca-opera-edit", function(e) {
            var t = $(e.currentTarget)
              , o = t.parent().find(".cca-oe")
              , a = $(".cca-opera-edit");
            t.hasClass("cca-edit-open") ? (t.removeClass("cca-edit-open"),
            o.fadeOut()) : (a.each(function(e, t) {
                $(t).hasClass("cca-edit-open") && ($(t).removeClass("cca-edit-open"),
                $(t).parent().find(".cca-oe").fadeOut())
            }),
            $(".cc-background").removeClass("hide"),
            t.addClass("cca-edit-open"),
            o.fadeIn())
        }),
        $(document).on("click", ".cc-background", function(e) {
            var t = ($(e.currentTarget),
            $(".cca-opera-edit"));
            t.each(function(e, t) {
                $(t).hasClass("cca-edit-open") && ($(t).removeClass("cca-edit-open"),
                $(t).parent().find(".cca-oe").fadeOut())
            }),
            $(".cc-background").addClass("hide")
        }),
        a.on("click", ".cca-oe-ding", function(e) {
            var t = $(e.currentTarget)
              , o = t.attr("mid")
              , a = t.parent().parent().parent().find(".cca-b-ding");
            t.parent().parent().parent().parent();
            t.hasClass("ding-comment-cca") ? window.enableDing ? $.ajax({
                url: window.comment_url + "novel/i.php?do=sp_top",
                data: {
                    act: "add",
                    authorId: authorId_cover,
                    sqUid: localStorage.userId,
                    mid: o
                },
                type: "GET",
                success: function(e) {
                    console.log(e),
                    console.log("置顶"),
                    "200" == e.status ? (t.html("取消置顶"),
                    t.removeClass("ding-comment-cca"),
                    a.removeClass("hide"),
                    window.enableDing = !1,
                    $(".cc-background").click(),
                    setTimeout(function() {
                        c(bookId_cover, authorId_cover),
                        d(bookId_cover, authorId_cover)
                    }, 1e3)) : messageAlert("warning", e.message)
                }
            }) : messageAlert("warning", "置顶评论只能有一条。") : $.ajax({
                url: window.comment_url + "novel/i.php?do=sp_top",
                data: {
                    act: "del",
                    authorId: authorId_cover,
                    sqUid: localStorage.userId,
                    mid: o
                },
                type: "GET",
                success: function(e) {
                    console.log("取消置顶"),
                    console.log(e),
                    "200" == e.status ? (t.html("置顶"),
                    t.addClass("ding-comment-cca"),
                    a.addClass("hide"),
                    window.enableDing = !0,
                    $(".cc-background").click(),
                    setTimeout(function() {
                        c(bookId_cover, authorId_cover),
                        d(bookId_cover, authorId_cover)
                    }, 1e3)) : messageAlert("warning", e.message)
                }
            })
        }),
        a.on("click", ".cca-oe-jing", function(e) {
            var t = $(e.currentTarget)
              , o = t.attr("mid")
              , a = t.parent().parent().parent().find(".cca-b-jing");
            t.parent().parent().find(".cca-opera-edit");
            t.hasClass("jing-comment-cca") ? $.ajax({
                url: window.comment_url + "novel/i.php?do=sp_jing",
                data: {
                    act: "add",
                    authorId: authorId_cover,
                    sqUid: localStorage.userId,
                    mid: o
                },
                type: "GET",
                success: function(e) {
                    console.log("加精"),
                    console.log(e),
                    "200" == e.status ? (t.html("取消加精"),
                    t.removeClass("jing-comment-cca"),
                    a.removeClass("hide"),
                    $(".cc-background").click()) : messageAlert("warning", e.message)
                }
            }) : $.ajax({
                url: window.comment_url + "novel/i.php?do=sp_jing",
                data: {
                    act: "del",
                    authorId: authorId_cover,
                    sqUid: localStorage.userId,
                    mid: o
                },
                type: "GET",
                success: function(e) {
                    console.log("取消加精"),
                    console.log(e),
                    "200" == e.status ? (t.html("加精"),
                    t.addClass("jing-comment-cca"),
                    a.addClass("hide"),
                    $(".cc-background").click()) : messageAlert("warning", e.message)
                }
            })
        }),
        a.on("click", ".cca-l-more-btn", function(e) {
            window.location.href = "./comment.php?bid=" + public.queryString().bid
        }),
        a.on("input", ".text-comment-cover-textarea-textarea", function(e) {
            var t = $(e.currentTarget)
              , o = $(".text-comment-cover-textarea-div-comment-btn")
              , a = t.val().length;
            a >= 5 && a <= 500 ? o.addClass("can-use-tcctdcb") : o.removeClass("can-use-tcctdcb")
        }),
        a.on("click", ".zk-comment-div", function(e) {
            var t = $(e.currentTarget);
            t.slideUp(),
            t.next("pre").slideDown()
        }),
        a.on("click", ".sq-comment-div", function(e) {
            var t = $(e.currentTarget);
            t.slideUp(),
            t.prev("pre").slideDown()
        }),
        a.on("click", ".cca-reply-btn", function(e) {
            var o = $(this).parent().parent().find(".replyshow");
            "none" == o.css("display") ? o.css("display", "block") : o.css("display", "none"),
            $(".cca-reply-box").fadeOut();
            var a = $(this).parent().parent().find(".cca-reply-box")
              , n = $(this).parent().parent().find(".content-reply-text")
              , i = $(this).parent().parent().find(".cca-lct-left").html();
            a.stop().fadeIn(),
            n.attr("placeholder", "回复" + i + ":").focus(),
            t($(this).parent().parent(), $(this).attr("mid"), "book-reply"),
            e.stopPropagation()
        }),
        a.on("click", ".js-comment-btn", function(e) {
            var t = $(e.currentTarget)
              , o = t.parent().find(".content-reply-text")
              , a = o.val()
              , n = t.attr("rootMid")
              , i = t.attr("rootUid")
              , c = ~~((new Date).getTime() / 1e3)
              , d = "sq_uid=" + localStorage.userId + "&sn=" + window.FingerprintCode + "&imei=" + window.FingerprintCode + "&appid=10000&app_time=" + c + "&key=" + sessionStorage.keyParams
              , l = md5(d).toString().toUpperCase();
            if (a = r(a),
            !a)
                return void messageAlert("warning", "回复评论不能为空！");
            var s = {
                appSignParms: "sq_uid:sn:imei:appid:app_time",
                app_time: c,
                authorId: authorId_cover,
                authorName: authorName_cover,
                bookId: bookId_cover,
                bookName: bookName_cover,
                imei: window.FingerprintCode,
                sign: l,
                sn: window.FingerprintCode,
                source: "store",
                sqUid: localStorage.userId || 8e6,
                text: a,
                rootMid: n,
                rootUid: i
            };
            $.ajax({
                url: window.comment_url + "novel/i.php?do=sp_reply",
                data: s,
                type: "POST",
                success: function(e) {
                    if (console.log("点击了回复"),
                    console.log(e),
                    200 == e.status) {
                        o.val(""),
                        $(".cca-reply-box").fadeOut();
                        var n = _.template($("#cca-reply-publish").html());
                        t.parent().parent().find(".user-reply-box").prepend(n({
                            replyFlag: !0,
                            mid: e.data.mid,
                            name: localStorage.nickname,
                            text: a
                        })),
                        messageAlert("success", "回复发表成功")
                    } else
                        10008 == e.status ? (messageAlert("warning", "请先登录才可以进行回复。"),
                        $("#login").dialog("open")) : messageAlert("warning", e.message)
                }
            })
        }),
        a.on("click", ".msg-reply", function(e) {
            $(".cca-reply-box").fadeOut(),
            $(this).parent().parent().find(".cca-reply-box").remove();
            var o = $(this).attr("rootUid")
              , a = $(this).attr("mid")
              , n = $(this).attr("uid")
              , i = $(this).parent().parent().find("span").html()
              , r = ($(this).attr("repliedUid"),
            $(this).attr("repliedMid"),
            $(this).attr("rootMid"))
              , c = '<div class="cca-reply-box mb0" style="display:none;">';
            c += '<div class="content-reply-inputbox fl">',
            c += '<input class="content-reply-text" maxlength="200" type="text" name="content-reply-text" placeholder="回复' + i + '：">',
            c += "</div>",
            c += '<input replyAuthor="' + i + '" mid="' + a + '" uid="' + n + '" rootUid="' + o + '" rootMid="' + r + '" class="comment-reply-btn js-reply-btn" type="button" value="回复">',
            c += "</div>",
            $(this).parent().parent().append(c),
            $(this).parent().parent().find(".cca-reply-box").stop().fadeIn(),
            $(this).parent().parent().find(".content-reply-text").focus(),
            t($(this).parent().parent().parent(), a, "author-reply", i),
            e.stopPropagation()
        }),
        a.on("click", ".js-reply-btn", function(e) {
            var t = $(e.currentTarget)
              , o = t.parent().find(".content-reply-text")
              , a = o.val()
              , n = t.attr("rootMid")
              , i = t.attr("rootUid")
              , c = t.attr("mid")
              , d = t.attr("uid")
              , l = ~~((new Date).getTime() / 1e3)
              , s = "sq_uid=" + localStorage.userId + "&sn=" + window.FingerprintCode + "&imei=" + window.FingerprintCode + "&appid=10000&app_time=" + l + "&key=" + sessionStorage.keyParams
              , m = md5(s).toString().toUpperCase();
            if (a = r(a),
            !a)
                return void messageAlert("warning", "回复评论不能为空！");
            var p = {
                appSignParms: "sq_uid:sn:imei:appid:app_time",
                app_time: l,
                authorId: authorId_cover,
                authorName: authorName_cover,
                bookId: bookId_cover,
                bookName: bookName_cover,
                imei: window.FingerprintCode,
                sign: m,
                sn: window.FingerprintCode,
                source: "store",
                sqUid: localStorage.userId || 8e6,
                text: a,
                rootMid: n,
                rootUid: i,
                repliedMid: c,
                repliedUid: d
            };
            $.ajax({
                url: window.comment_url + "novel/i.php?do=sp_reply",
                data: p,
                type: "POST",
                success: function(e) {
                    if (200 == e.status) {
                        o.val(""),
                        $(".cca-reply-box").fadeOut();
                        var n = _.template($("#cca-reply-publish").html());
                        t.parent().parent().after(n({
                            replyFlag: !1,
                            mid: e.data.mid,
                            replyAuthor: t.attr("replyauthor"),
                            name: localStorage.nickname,
                            text: a
                        })),
                        messageAlert("success", "回复发表成功")
                    } else
                        10008 == e.status ? (messageAlert("warning", "请先登录才可以进行回复。"),
                        $("#login").dialog("open")) : messageAlert("warning", e.message)
                }
            })
        }),
        a.on("click", ".comment-info-move", function() {
            var e = $(this)
              , t = {
                page: $(this).attr("page"),
                size: 10,
                authorId: authorId_cover,
                mid: $(this).attr("mid"),
                sqUid: localStorage.userId || 8e6
            };
            $.ajax({
                url: window.comment_url + "novel/i.php?do=sp_info",
                data: t,
                type: "GET",
                success: function(t) {
                    if (200 == t.status) {
                        var o = _.template($("#bk_sp_info_tpl").html());
                        e.parent().append(o({
                            data: t.data,
                            info: t.info
                        })),
                        e.remove()
                    }
                }
            })
        }),
        $(document).on("click", ".content-reply-text", function(e) {
            e.stopPropagation()
        }),
        $(document).on("click", function() {
            $(".cca-reply-box").fadeOut()
        }),
        o(),
        s(function(t) {
            1 == t.length && $(".cover-chapter-right").addClass("hide");
            for (var o = 0; o < t.length; o++)
                e(t[o].module_id, t[o].module_name, o)
        })
    }),
    $(document).on("click", ".title-comment-cover-right", function() {
        window.location.href = "./comment.php?bid=" + public.queryString().bid
    })
}();
