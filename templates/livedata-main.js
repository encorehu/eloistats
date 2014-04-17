{% set intCountShares = globals().get('intCountShares', '1') %}
	var intCountShares = {{intCountShares}};
	var intSharesPerUnit = (10.581333333333) * 0.02;
	var intCurrentBlockHeight = 1;
	var intCurrentBlockConfirms = 0;
	var latestBlockHeight = 1;
	var latestBlockConfirms = 0;
	var intRoundDuration = 1;
	var prettyRoundDuration = '';
	var prettyHashrate = '908.93 Gh/s';
	var networkDifficulty = 6119726089.1281;
	var networkDifficulty1000 = networkDifficulty * 1000;
	var dom_livehashrate;
	var dom_liveluck;
	var dom_roundtime;
	var dom_sharecounter;
	var countSharesDelay;
	var countSharesDelayNext = 41;

	function updateRoundDuration()
	{
		prettyRoundDuration = secondsToHms(intRoundDuration);
		dom_roundtime.data = prettyRoundDuration;
		intRoundDuration++;
	}

	function updateLuck()
	{
		var luck = Math.round( networkDifficulty1000 / intCountShares ) / 10;
		var newstr;
		if (luck > 9999.9) {
			newstr = '>9999.9%';
		} else {
			if (luck >= 1000.0) {
				newstr = Math.round(luck) + '%';
			} else {
				newstr = luck + '%';
			}
		}
		if (dom_liveluck.data != newstr)
			dom_liveluck.data = newstr;
	}

	function updatePerSecond()
	{
		updateRoundDuration();
		updateLuck();
		setTimeout("updatePerSecond()",1000);
	}

	function updateSharesData()
	{

		$.getJSON("/instant/livedata.json?rand=" + Math.random(),
			function(data){
				intCountShares = data.roundsharecount;
				intSharesPerUnit = data.sharesperunit * 0.02;
				latestBlockHeight = data.lastblockheight;
				latestBlockConfirms = data.lastconfirms;
				intRoundDuration = data.roundduration;
				prettyHashrate = data.hashratepretty;
				networkDifficulty = data.network_difficulty;
				networkDifficulty1000 = networkDifficulty * 1000;

				dom_livehashrate.data = prettyHashrate;
			});

		setTimeout("updateSharesData()",60000);
		setTimeout("checkNewInfo()",500);
	}

	function checkNewInfo()
	{
		if (latestBlockHeight != intCurrentBlockHeight) {
			// new block found... add it!
			$.getJSON("/instant/blockinfo.json?height="+latestBlockHeight+"&cclass="+$("#blocklisttable tr:last").attr('class'),
				function(data){
					$("#blocklistheaderid").after(data.blockrow);
					$("#blocklisttable tr:last").remove();
					intCurrentBlockHeight = latestBlockHeight;
				});
		}

		if (latestBlockConfirms != intCurrentBlockConfirms) {
			// new confirmation data...
			intCurrentBlockConfirms = latestBlockConfirms;
			updateBlockTable(0);

		}
	}

	function countShares()
	{
		intCountShares += intSharesPerUnit * countSharesDelay;
		dom_sharecounter.data = Math.round(intCountShares);
		countSharesDelay = countSharesDelayNext;
		setTimeout("countShares()", countSharesDelay);
	}

	$(window).blur(function() {
		countSharesDelayNext = 1318;
	})

	$(window).focus(function() {
		countSharesDelayNext = 41;
	})

	function initShares()
	{
		dom_livehashrate = document.getElementById('livehashrate').childNodes[0];
		dom_liveluck = document.getElementById('liveluck').childNodes[0];
		dom_roundtime = document.getElementById('roundtime').childNodes[0];
		dom_sharecounter = document.getElementById('sharecounter').childNodes[0];

		updateSharesData();
		updatePerSecond();
		countShares();

		setTimeout("updateBlockTable(1)",601000);

	}

	function updateBlockRow(relem, rblockid) {

			$.getJSON("/instant/blockinfo.json?dbid="+rblockid+"&cclass="+$(relem).attr('class'),
				function(data){
					$(relem).after(data.blockrow);
					$(relem).remove();
				});

	}

	function updateBlockTable(timercall)
	{

		$('#blocklisttable tr').each(function(index, elem) {
			if (index>0) {
				if ($(elem).attr('id').substring(0,8) == 'blockrow') {
					var confcell = 'null';
					$(elem).each(function() { confcell = $(this).find('.blockconfirms').html(); });
					if (!((confcell == 'Confirmed') || (confcell == 'Stale'))) {
						updateBlockRow(elem,$(elem).attr('id').substring(8));
					}
				}
			}

		});
		if (timercall) {
			setTimeout("updateBlockTable(1)",601000);
		}

	}

	function secondsToHms(d) {
		d = Number(d);
		var h = Math.floor(d / 3600);
		var m = Math.floor(d % 3600 / 60);
		var s = Math.floor(d % 3600 % 60);
		return ((h > 0 ? h + ":" : "") + (m >= 0 ? (h > 0 && m < 10 ? "0" : "") + m + ":" : "0:") + (s < 10 ? "0" : "") + s);
	}

