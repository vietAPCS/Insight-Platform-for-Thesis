let django_url = my_url
let token = csrftoken

function viewSign(mess){
  alert(mess);
}

async function sign(id, mess){
  if (!window.ethereum) {
    alert('Metamask not installed')
    return null;
  }

  try{
    const provider = new ethers.providers.Web3Provider(window.ethereum)
    await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner()
    if(signer == null) return;
    const signature = await signer.signMessage(mess);

    if (signature){
      let formData2 = new FormData();
      formData2.append('id', id);
      formData2.append('signature', signature);

      let ret = await fetch(django_url,{
        method: "POST",
        body: formData2,
        headers: {
          "X-CSRFToken": token,
        }})
        .then((response) =>{
          if (response.ok) {
            alert('Successful!');
            location.reload();
          }
          else alert('fail to sign');
        })
    }
  } catch (error) {
    console.error(error);
  }
}

async function signScore(id){
  if (!window.ethereum) {
    alert('Metamask not installed')
    return null;
  }

  try{
    let score = document.getElementById('score'+id).value;
    let mess = score.toString();

    const provider = new ethers.providers.Web3Provider(window.ethereum)
    await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner()
    if(signer == null) return;
    const signature = await signer.signMessage(mess+id);

    if (signature){
      let formData2 = new FormData();
      formData2.append('id', id);
      formData2.append('score', score);
      formData2.append('score_signature', signature);

      let ret = await fetch(django_url,{
        method: "POST",
        body: formData2,
        headers: {
          "X-CSRFToken": token,
        }})
        .then((response) =>{
          if (response.ok) {
            alert('Successful!');
            location.reload();
          }
          else alert('fail to sign');
        })
    }
  } catch (error) {
    console.error(error);
  }
}

async function signFile(id, file) { 

  if (!window.ethereum) {
    alert('Metamask not installed')
    return null;
  }

  // try{
    let formData = new FormData();
    formData.append('id', id);
    formData.append('doc', file.files[0]);

    let data = await fetch(django_url,{
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": token,
      }})
    .then(response => response.json());

    const mess = data.cid
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner();
    if(signer == null) return;
    const signature = await signer.signMessage(mess);

    if (signature){
      let formData2 = new FormData();
      formData2.append('id', id);
      formData2.append('signature', signature);

      let ret = await fetch(django_url,{
        method: "POST",
        body: formData2,
        headers: {
          "X-CSRFToken": token,
        }})
        .then((response) =>{
          if (response.ok) {
            alert('Successful!');
            location.reload();
          }
          else alert('fail to sign');
        })
    }
    
  // } catch (error) {
  //   console.error(error);
  // }
}