var data1 = [
    { STT: '1', hoten: 'Nguyễn Minh Tú',lop:"12A1",gioitinh:"Nam",namsinh:"2001",diachi:"100 Quang Trung"},
            { STT: '2', hoten: 'Nguyễn Minh Hùng',lop:"12A2",gioitinh:"Nam",namsinh:"2001",diachi:"105 Quang Trung"}
]
        var data2 = [
    { STT: '3', hoten: 'Lê Thị Thu',lop:"Chưa có",gioitinh:"Nữ",namsinh:"1999",diachi:"50 Quang Trung"}
]
        function insertDatatoTable(data){
            for(var i=0;i<data.length;i++) {
                            var stt=data[i]["STT"];
                            var hoten=data[i]["hoten"];
                            var lop=data[i]["lop"];
                            var gioitinh=data[i]["gioitinh"];
                            var namsinh=data[i]["namsinh"];
                            var diachi=data[i]["diachi"];

                            var table=document.getElementsByTagName("table")[0];

                            var newRow=table.insertRow(table.rows.length);
                            var cell1=newRow.insertCell(0);
                            var cell2=newRow.insertCell(1);
                            var cell3=newRow.insertCell(2);
                            var cell4=newRow.insertCell(3);
                            var cell5=newRow.insertCell(4);
                            var cell6=newRow.insertCell(5);

                            cell1.innerHTML=stt;
                            cell2.innerHTML=hoten;
                            cell3.innerHTML=lop;
                            cell4.innerHTML=gioitinh;
                            cell5.innerHTML=namsinh;
                            cell6.innerHTML=diachi;
                        }
        }
        function DeleteCurTable()
        {
            var table=document.getElementsByTagName("table")[0];
            if(table.rows.length>1)
            {
                for(var i=table.rows.length-1;i>=1;i--)
                {
                    table.deleteRow(i);
                }
            }
        }
        function update(){
            var select = document.getElementById('haveclass?');
            var option = select.options[select.selectedIndex].text;
            if(option=="Học sinh có lớp")
            {
                DeleteCurTable();
                insertDatatoTable(data1);
            }
            else
            {
                DeleteCurTable();
                insertDatatoTable(data2);
            }
        }
